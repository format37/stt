from aiohttp import web
import uuid
import contextlib
import glob
import json
import os
from pathlib import Path
from typing import Optional
import pytorch_lightning as pl
import torch
import shutil
from nemo.collections.asr.metrics.rnnt_wer import RNNTDecodingConfig
from nemo.collections.asr.models import ASRModel
from nemo.collections.asr.models.ctc_models import EncDecCTCModel
from nemo.collections.asr.parts.utils.transcribe_utils import transcribe_partial_audio
from nemo.utils import logging, model_utils


class TranscriptionConfig:
    # Required configs
    model_path: Optional[str] = 'model/stt_ru_quartznet15x5.nemo'  # Path to a .nemo file
    pretrained_name: Optional[str] = 'stt_ru_quartznet15x5'  # Name of a pretrained model
    audio_dir: Optional[str] = '/server/audio'  # Path to a directory which contains audio files
    dataset_manifest: Optional[str] = None  # Path to dataset's JSON manifest

    # General configs
    output_filename: Optional[str] = 'result.txt'
    batch_size: int = 32
    num_workers: int = 0

    # Set `cuda` to int to define CUDA device. If 'None', will look for CUDA
    # device anyway, and do inference on CPU only if CUDA device is not found.
    # If `cuda` is a negative number, inference will be on CPU only.
    cuda: Optional[int] = None
    amp: bool = False
    audio_type: str = "wav"

    # Recompute model transcription, even if the output folder exists with scores.
    overwrite_transcripts: bool = True

    # Decoding strategy for CTC models
    # ctc_decoding: CTCDecodingConfig = CTCDecodingConfig() #  debug

    # Decoding strategy for RNNT models
    rnnt_decoding: RNNTDecodingConfig = RNNTDecodingConfig(fused_batch_size=-1)


async def call_test(request):
    content = "get ok"
    return web.Response(text=content, content_type="text/html")


async def call_inference(request):
    
    cfg = TranscriptionConfig()
     
    # Get the audio file data from the request
    audio_file_data = await request.post()
    audio_file_data = audio_file_data['file'].file.read()
    # Create a temporary directory for the audio file
    tmp_dir = '/server/audio/'+str(uuid.uuid4())
    os.mkdir(tmp_dir)
    # Write the audio file data to the temporary directory
    audio_file_path = tmp_dir + '/' + str(uuid.uuid4()) + '.wav'
    with open(audio_file_path, 'wb') as f:
        f.write(audio_file_data)    
    cfg.audio_dir = str(tmp_dir)

    if cfg.model_path is None and cfg.pretrained_name is None:
        raise ValueError("Both cfg.model_path and cfg.pretrained_name cannot be None!")
    if cfg.audio_dir is None and cfg.dataset_manifest is None:
        raise ValueError("Both cfg.audio_dir and cfg.dataset_manifest cannot be None!")

    # setup GPU
    if cfg.cuda is None:
        if torch.cuda.is_available():
            device = [0]  # use 0th CUDA device
            accelerator = 'gpu'
        else:
            device = 1
            accelerator = 'cpu'
    else:
        device = [cfg.cuda]
        accelerator = 'gpu'

    map_location = torch.device('cuda:{}'.format(device[0]) if accelerator == 'gpu' else 'cpu')

    # setup model
    if cfg.model_path is not None:
        # restore model from .nemo file path
        model_cfg = ASRModel.restore_from(restore_path=cfg.model_path, return_config=True)
        classpath = model_cfg.target  # original class path
        imported_class = model_utils.import_class_by_path(classpath)  # type: ASRModel
        logging.info(f"Restoring model : {imported_class.__name__}")
        asr_model = imported_class.restore_from(
            restore_path=cfg.model_path, map_location=map_location
        )  # type: ASRModel
        model_name = os.path.splitext(os.path.basename(cfg.model_path))[0]
    else:
        # restore model by name
        asr_model = ASRModel.from_pretrained(
            model_name=cfg.pretrained_name, map_location=map_location
        )  # type: ASRModel
        model_name = cfg.pretrained_name

    trainer = pl.Trainer(devices=device, accelerator=accelerator)
    asr_model.set_trainer(trainer)
    asr_model = asr_model.eval()
    partial_audio = False

    # Setup decoding strategy
    if hasattr(asr_model, 'change_decoding_strategy'):
        # Check if ctc or rnnt model
        if hasattr(asr_model, 'joint'):  # RNNT model
            asr_model.change_decoding_strategy(cfg.rnnt_decoding)

    # get audio filenames
    if cfg.audio_dir is not None:
        filepaths = list(glob.glob(os.path.join(cfg.audio_dir, f"**/*.{cfg.audio_type}"), recursive=True))
    else:
        # get filenames from manifest
        filepaths = []
        if os.stat(cfg.dataset_manifest).st_size == 0:
            logging.error(f"The input dataset_manifest {cfg.dataset_manifest} is empty. Exiting!")
            return None

        manifest_dir = Path(cfg.dataset_manifest).parent
        with open(cfg.dataset_manifest, 'r') as f:
            has_two_fields = []
            for line in f:
                item = json.loads(line)
                if "offset" in item and "duration" in item:
                    has_two_fields.append(True)
                else:
                    has_two_fields.append(False)
                audio_file = Path(item['audio_filepath'])
                if not audio_file.is_file() and not audio_file.is_absolute():
                    audio_file = manifest_dir / audio_file
                filepaths.append(str(audio_file.absolute()))
        partial_audio = all(has_two_fields)

    logging.info(f"\nTranscribing {len(filepaths)} files...\n")

    # setup AMP (optional)
    if cfg.amp and torch.cuda.is_available() and hasattr(torch.cuda, 'amp') and hasattr(torch.cuda.amp, 'autocast'):
        logging.info("AMP enabled!\n")
        autocast = torch.cuda.amp.autocast
    else:

        @contextlib.contextmanager
        def autocast():
            yield

    # Compute output filename
    if cfg.output_filename is None:
        # create default output filename
        if cfg.audio_dir is not None:
            cfg.output_filename = os.path.dirname(os.path.join(cfg.audio_dir, '.')) + '.json'
        else:
            cfg.output_filename = cfg.dataset_manifest.replace('.json', f'_{model_name}.json')

    # if transcripts should not be overwritten, and already exists, skip re-transcription step and return
    if not cfg.overwrite_transcripts and os.path.exists(cfg.output_filename):
        logging.info(
            f"Previous transcripts found at {cfg.output_filename}, and flag `overwrite_transcripts`"
            f"is {cfg.overwrite_transcripts}. Returning without re-transcribing text."
        )

        # remove tmp_dir with files
        shutil.rmtree(tmp_dir)
        msg = 'transcripts should not be overwritten, and already exists, skip re-transcription step'
        return web.Response(text=msg, content_type="text/html")

    # transcribe audio
    with autocast():
        with torch.no_grad():
            if partial_audio:
                if isinstance(asr_model, EncDecCTCModel):
                    transcriptions = transcribe_partial_audio(
                        asr_model=asr_model,
                        path2manifest=cfg.dataset_manifest,
                        batch_size=cfg.batch_size,
                        num_workers=cfg.num_workers,
                    )
                else:
                    logging.warning(
                        "RNNT models do not support transcribe partial audio for now. Transcribing full audio."
                    )
                    transcriptions = asr_model.transcribe(
                        paths2audio_files=filepaths, batch_size=cfg.batch_size, num_workers=cfg.num_workers,
                    )
            else:
                transcriptions = asr_model.transcribe(
                    paths2audio_files=filepaths, batch_size=cfg.batch_size, num_workers=cfg.num_workers,
                )

    logging.info(f"Finished transcribing {len(filepaths)} files !")

    logging.info(f"Writing transcriptions into file: {cfg.output_filename}")

    # if transcriptions form a tuple (from RNNT), extract just "best" hypothesis
    if type(transcriptions) == tuple and len(transcriptions) == 2:
        transcriptions = transcriptions[0]
    # write audio transcriptions
    with open(cfg.output_filename, 'w', encoding='utf-8') as f:
        if cfg.audio_dir is not None:
            for idx, text in enumerate(transcriptions):
                item = {'audio_filepath': filepaths[idx], 'pred_text': text}
                f.write(json.dumps(item) + "\n")
        else:
            with open(cfg.dataset_manifest, 'r') as fr:
                for idx, line in enumerate(fr):
                    item = json.loads(line)
                    item['pred_text'] = transcriptions[idx]
                    f.write(json.dumps(item) + "\n")

    logging.info("Finished writing predictions !")

    # remove tmp_dir with files
    shutil.rmtree(tmp_dir)

    # return json dumped item
    return web.Response(text=json.dumps(item), content_type="text/html")


def main():
    app = web.Application(client_max_size=1024**3)
    app.router.add_route('GET', '/test', call_test)
    app.router.add_route('POST', '/inference', call_inference)
    web.run_app(app, port=os.environ.get('PORT', ''))


if __name__ == "__main__":
    main()
