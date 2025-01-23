from stt import transcribe_multiple_languages

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
