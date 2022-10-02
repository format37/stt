import io
import os
from google.cloud import speech_v1p1beta1


def transcribe_google(language, file_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'api.json'
    # language = 'ru'
    client = speech_v1p1beta1.SpeechClient()
    sample_rate_hertz = 8000
    encoding = speech_v1p1beta1.RecognitionConfig.AudioEncoding.MP3

    config = {
        "language_code": language,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
    }
    with io.open(file_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = speech_v1p1beta1.RecognitionAudio(content=content)

        response = client.recognize(config=config, audio=audio)
        results = []
        for result in response.results:
            alternative = result.alternatives[0]
            results.append(alternative.transcript)
    return ''.join([str(item) for item in results]).lower()


def main():
    transcribation = transcribe_google('en', 'telegram.ogg')
    print(transcribation)


if __name__ == '__main__':
    main()
