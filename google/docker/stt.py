from typing import List
from google.cloud import speech_v1 as speech

def transcribe_multiple_languages(audio_file: str, language_codes: List[str]):
    """Transcribe an audio file using Google Cloud Speech-to-Text API with support for multiple languages.

    Args:
        audio_file (str): Path to the local audio file to be transcribed.
        language_codes (List[str]): A list of BCP-47 language codes for transcription.

    Returns:
        None: Prints the transcription results.
    """
    client = speech.SpeechClient()

    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        audio_content = f.read()

    config = {
        "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
        "language_code": language_codes[0],  # Primary language
        "alternative_language_codes": language_codes[1:],  # Alternative languages
        "model": "latest_long"  # Use the latest model
    }

    audio = {"content": audio_content}
    
    response = client.recognize(config=config, audio=audio)

    return response

# Example usage
if __name__ == "__main__":
    audio_file_path = "in.wav"  # Replace with your audio file path
    with open("BCP-47.txt", "r") as f:  # https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages
        languages = [line.strip() for line in f if line.strip()]
    response = transcribe_multiple_languages(audio_file_path, languages)
    for result in response.results:
        detected_language = result.language_code  # Get detected language code
        print(f"Detected Language: {detected_language}")
        print(f"Transcript: {result.alternatives[0].transcript}")
