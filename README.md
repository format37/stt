# Speech to text transcribation services
### Cloning the repository
git clone https://github.com/format37/stt.git
cd stt
## Kaldi Vosk speech to text transcribation GPU docker server
#### Installation
```
cd vosk
pip install -r requirements.txt
```
#### Download the model
Choose your language:  
* English
```
wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
unzip vosk-model-en-us-0.22.zip
mv vosk-model-en-us-0.22 model
rm vosk-model-en-us-0.22.zip
```
* Russian
```
wget https://alphacephei.com/vosk/models/vosk-model-ru-0.10.zip
unzip vosk-model-ru-0.10.zip
mv vosk-model-ru-0.10 model
rm vosk-model-ru-0.10.zip
```
* Another languages:  
[List of models](https://alphacephei.com/vosk/models)
#### Build
```
docker-compose up -d
```
#### Using
```
python asr-test.py en.wav
```
#### Troubles
It should be a Mono audio file, with Sample rate, the same as set in docker-compose.yml  
To prepare audio file we can use this command:
```
ffmpeg -i audio.wav -ac 1 -ar 16000 audio_prepared.wav
```
#### Thanks to
This container based on Sergey Korol's [repository](https://github.com/sskorol/vosk-api-gpu) and his [docker image](https://hub.docker.com/r/sskorol/vosk-api/tags)
