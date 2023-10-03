FROM alphacep/kaldi-vosk-server-gpu:latest

# Set environment variable for the model filename without extension
ENV MODEL_FILENAME vosk-model-en-us-0.42-gigaspeech

# Change to the working directory
RUN cd /opt/vosk-server/websocket-gpu-batch

# Copy the model zip file into the container
COPY ${MODEL_FILENAME}.zip /opt/vosk-server/websocket-gpu-batch

# Set the working directory inside the container
WORKDIR /opt/vosk-server/websocket-gpu-batch

# Unzip the model, move it, and clean up
RUN \
   unzip ${MODEL_FILENAME}.zip \
   && mv ${MODEL_FILENAME} model \
   && rm -rf ${MODEL_FILENAME}.zip

# Copy the model configuration
COPY model.conf /opt/vosk-server/websocket-gpu-batch/model/conf/

# Expose the port the app runs on
EXPOSE 2700

# Command to run the application
CMD [ "python3", "./asr_server_gpu.py" ]
