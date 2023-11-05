from pydub import AudioSegment

# Load your existing MP3 file
# audio = AudioSegment.from_file("output_2023-11-05_12-20-43.mp3", format="mp3")
audio = AudioSegment.from_file("audio_2023-11-06_00-20-21.ogg", format="mp3")

# Change the frame rate to 16000 Hz
audio = audio.set_frame_rate(16000)

# Export the result
audio.export("output_2023-11-05_12-20-43.mp3", format="mp3")
