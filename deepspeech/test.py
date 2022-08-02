from deepspeech import Model
import wave
import numpy as np


def metadata_to_string(metadata):
    return ''.join(token.text for token in metadata.tokens)


ds = Model('deepspeech-0.9.3-models.pbmm')

fin = wave.open('audio/2830-3980-0043.wav', 'rb')
fs_orig = fin.getframerate()
audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

audio_length = fin.getnframes() * (1/fs_orig)
fin.close()

print(ds.stt(audio))
