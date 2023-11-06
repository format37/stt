FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ru.mp3 ru.mp3

COPY app.py app.py

VOLUME /app/cache

ENTRYPOINT ["python3", "app.py"]