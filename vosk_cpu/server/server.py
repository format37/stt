from aiohttp import web
import os
import json
import soundfile as sf
import torch
from nemo.collections.tts.models.base import SpectrogramGenerator, Vocoder
import uuid


def load_spectrogram_model():
    override_conf = None
    
    from_pretrained_call = SpectrogramGenerator.from_pretrained
    
    if spectrogram_generator == "tacotron2":
        from nemo.collections.tts.models import Tacotron2Model
        pretrained_model = "tts_en_tacotron2"
    elif spectrogram_generator == "fastpitch":
        from nemo.collections.tts.models import FastPitchModel
        pretrained_model = "tts_en_fastpitch"
    elif spectrogram_generator == "mixertts":
        from nemo.collections.tts.models import MixerTTSModel
        pretrained_model = "tts_en_lj_mixertts"
    elif spectrogram_generator == "mixerttsx":
        from nemo.collections.tts.models import MixerTTSModel
        pretrained_model = "tts_en_lj_mixerttsx"
    else:
        raise NotImplementedError
        
    model = from_pretrained_call(pretrained_model, override_config_path=override_conf)
    
    return model


def load_vocoder_model():
    TwoStagesModel = False
    strict=True
    
    if audio_generator == "waveglow":
        from nemo.collections.tts.models import WaveGlowModel
        pretrained_model = "tts_waveglow"
        strict=False
    elif audio_generator == "hifigan":
        from nemo.collections.tts.models import HifiGanModel
        spectrogram_generator2ft_hifigan = {
            "mixertts": "tts_en_lj_hifigan_ft_mixertts",
            "mixerttsx": "tts_en_lj_hifigan_ft_mixerttsx"
        }
        pretrained_model = spectrogram_generator2ft_hifigan.get(spectrogram_generator, "tts_hifigan")
    elif audio_generator == "univnet":
        from nemo.collections.tts.models import UnivNetModel
        pretrained_model = "tts_en_lj_univnet"
    elif audio_generator == "griffin-lim":
        from nemo.collections.tts.models import TwoStagesModel
        cfg = {'linvocoder':  {'_target_': 'nemo.collections.tts.models.two_stages.GriffinLimModel',
                             'cfg': {'n_iters': 64, 'n_fft': 1024, 'l_hop': 256}},
               'mel2spec': {'_target_': 'nemo.collections.tts.models.two_stages.MelPsuedoInverseModel',
                           'cfg': {'sampling_rate': 22050, 'n_fft': 1024, 
                                   'mel_fmin': 0, 'mel_fmax': 8000, 'mel_freq': 80}}}
        model = TwoStagesModel(cfg)            
        TwoStagesModel = True
    else:
        raise NotImplementedError

    if not TwoStagesModel:
        model = Vocoder.from_pretrained(pretrained_model, strict=strict)
        
    return model


def infer(spec_gen_model, vocoder_model, str_input):
    parser_model = spec_gen_model
    with torch.no_grad():
        parsed = parser_model.parse(str_input)
        gen_spec_kwargs = {}
        
        if spectrogram_generator == "mixerttsx":
            gen_spec_kwargs["raw_texts"] = [str_input]
        
        spectrogram = spec_gen_model.generate_spectrogram(tokens=parsed, **gen_spec_kwargs)
        audio = vocoder_model.convert_spectrogram_to_audio(spec=spectrogram)
        
        if audio_generator == "hifigan":
            audio = vocoder_model._bias_denoise(audio, spectrogram).squeeze(1)
    if spectrogram is not None:
        if isinstance(spectrogram, torch.Tensor):
            spectrogram = spectrogram.to('cpu').numpy()
        if len(spectrogram.shape) == 3:
            spectrogram = spectrogram[0]
    if isinstance(audio, torch.Tensor):
        audio = audio.to('cpu').numpy()
    return spectrogram, audio.transpose()


async def call_test(request):
    content = "get ok"
    return web.Response(text=content, content_type="text/html")


async def call_inference(request):
    request_str = json.loads(str(await request.text()))
    data = json.loads(request_str)
    spec, audio = infer(spec_gen, vocoder, data['text'])

    # save audio to file with random filename    
    audio_file = "audio_" + str(uuid.uuid4()) + ".wav"
    sf.write(audio_file, audio, 22050, subtype='PCM_16')
    
    # return audio_file as binary data
    with open(audio_file, "rb") as f:
        audio_data = f.read()
        os.remove(audio_file)
        return web.Response(body=audio_data, content_type="audio/wav")    


def main():
    app = web.Application(client_max_size=1024**3)
    app.router.add_route('GET', '/test', call_test)
    app.router.add_route('POST', '/inference', call_inference)
    web.run_app(app, port=os.environ.get('PORT', ''))


spectrogram_generator = os.environ.get('SPECTROGRAM_GENERATOR', '')  #'tacotron2'
audio_generator = os.environ.get('AUDIO_GENERATOR', '')  # 'waveglow'

spec_gen = load_spectrogram_model().eval().cuda()
vocoder = load_vocoder_model().eval().cuda()


if __name__ == "__main__":
    main()
