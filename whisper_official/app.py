import whisper

model = whisper.load_model("large", download_root='/app/cache')
result = model.transcribe(
    "ru.mp3",
    language="ru",
    temperature=0.8,
    prompt="Звонок в сервисный центр по ремонту бытовой техники."
    )
print(result["text"])
