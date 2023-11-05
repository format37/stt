import torch
from transformers import (
    AutoModelForSpeechSeq2Seq, 
    AutoProcessor, 
    pipeline,
    )
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# model_id = "distil-whisper/distil-large-v2"
model_id = 'mitchelldehaven/whisper-large-v2-ru'

cache_dir = "/app/cache"

processor = AutoProcessor.from_pretrained(model_id)

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, 
    torch_dtype=torch_dtype,
    cache_dir=cache_dir
)

model.to(device)
tokenizer = processor.tokenizer

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=15,
    batch_size=16,
    torch_dtype=torch_dtype,
    device=device
)

sample = "ru.mp3"

start_time = time.time()
result = pipe(sample)
end_time = time.time()
print("\nTranscription:")
print(result["text"])
print("\nElapsed time: " + str(end_time - start_time) + " seconds")
# print result structure
print("\nResult structure:")
print(result)
