# NeMo ASR
Docker server, receives audio file over http post request  
And responses with transcribed text data  
### Installation
```
git clone https://github.com/format37/tts.git
cd tts/nemo/server/
```
### Download the model
* Select the [model](https://catalog.ngc.nvidia.com/orgs/nvidia/collections/nemo_asr)  
* Update wget string in model/download_model.sh
* run download_model.sh
```
cd model
sh download_model.sh
```

### Settings
Check docker-compose.yml to GPU / CPU settings.  
Comment GPU section, if you have no GPU (not tested).

### Build
sh compose.sh

### Using
[client.ipynb](https://github.com/format37/stt/blob/main/nemo/client/client.ipynb)
### Example
Text:  
```
сегодня ожидается хороший погод беросадков температуры воздуха деви зиградусов
```
[audio.wav](https://github.com/format37/stt/raw/main/nemo/client/ru.wav)
### Based on
[NVIDIA NeMo examples](https://github.com/NVIDIA/NeMo/blob/main/examples/asr/transcribe_speech.py)
### P.S.
In the NeMo examples path, (multi gpu inferense)[https://github.com/NVIDIA/NeMo/blob/main/examples/asr/transcribe_speech_parallel.py] is also available. U can implement it the same way.
