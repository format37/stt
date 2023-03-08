from flask import Flask, request
import logging
import os
import uuid
import io
from google.cloud import speech_v1p1beta1


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting server")

app = Flask(__name__)


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


@app.route("/test")
def call_test():
    return "get ok"


@app.route("/inference", methods=['POST'])
def call_inference():
    # get the request
    request_id = str(uuid.uuid4())

    # get the file
    file = request.files['file']
    logger.info("Received file %s", file.filename)

    # save the file
    file_path = os.path.join('data', request_id + '.ogg')
    file.save(file_path)

    # The request send like: r = requests.post(url, files={'file': f}, data={'language_code': language_code})
    # get the language code
    language_code = request.form.get('language_code', '')
    logger.info("Language code: %s", language_code)

    # transcribe
    transcribation = transcribe_google(language_code, file_path)
    logger.info("Transcribation: %s", transcribation)

    # remove file
    os.remove(file_path)

    # return the transcribation
    return transcribation


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=os.environ.get('PORT', ''))
