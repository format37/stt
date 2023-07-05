FROM alphacep/kaldi-vosk-server-gpu:latest

ENV MODEL_VERSION 0.42
RUN cd /opt/vosk-server/websocket-gpu-batch
COPY vosk-model-ru-${MODEL_VERSION}.zip /opt/vosk-server/websocket-gpu-batch
WORKDIR /opt/vosk-server/websocket-gpu-batch
RUN \
   unzip vosk-model-ru-${MODEL_VERSION}.zip \
   && mv vosk-model-ru-${MODEL_VERSION} model \
   && rm -rf vosk-model-ru-${MODEL_VERSION}.zip
COPY model.conf /opt/vosk-server/websocket-gpu-batch/model/conf/

EXPOSE 2700

CMD [ "python3", "./asr_server_gpu.py" ]
