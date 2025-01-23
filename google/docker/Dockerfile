FROM python:3.9.13-slim-buster
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY api.json /app
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/api.json"
COPY in.wav /app
COPY BCP-47.txt /app
COPY stt.py /app
COPY server.py /app
ENTRYPOINT ["python"]
CMD ["server.py"]