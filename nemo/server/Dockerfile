# FROM nemo:latest
FROM nvcr.io/nvidia/nemo:22.04
WORKDIR /server
COPY requirements.txt /server/
RUN pip install -r requirements.txt
RUN mkdir -p /server/audio/
COPY server.py /server/
ENTRYPOINT ["python3"]
CMD ["server.py"]