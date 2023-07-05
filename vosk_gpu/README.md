# Kaldi Vosk speech to text transcribation GPU docker server
Russian language example.  
Other languages are available at [alphacephei.com](https://alphacephei.com/vosk/models)
### Cloning the repository
```
git clone https://github.com/format37/stt.git
cd stt/vosk_gpu
```
#### Downloading the model
```
sh download_model.sh
```
#### Build
```
sh build.sh
```
#### Using
```
python asr-test.py ru.wav
```
Expected output:
```
# 1.0 0.03 0.48 сегодня
# 1.0 0.48 1.05 ожидается
# 0.815444 1.05 1.53 хорошая
# 1.0 1.56 2.01 погода
# 1.0 2.1 2.37 без
# 1.0 2.37 2.94 осадков
# 0.733007 3.0 3.72 температура
# 1.0 3.75 4.32 воздуха
# 0.994443 4.38 4.86 девять
# 1.0 4.86 5.46 градусов
=== middle confidence: 0.9542893999999998 

['сегодня ожидается хорошая погода без осадков температура воздуха девять градусов']
```
#### File format
It should be a Mono audio file, with Sample rate, the same as set in docker-compose.yml  
To prepare audio file we can use this command:
```
ffmpeg -i audio.wav -ac 1 -ar 16000 -ab 256k audio_prepared.wav
```
#### Thanks to
[alphacephei.com](https://alphacephei.com/vosk/)