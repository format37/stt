# Kaldi Vosk speech to text transcribation GPU docker server
### Cloning the repository
```
git clone https://github.com/format37/stt.git
cd stt/vosk_gpu
```
#### Build
```
sh compose
```
#### Using
```
cd client
python asr-test.py en.wav
```
Expected output:
```
# 1.0 1.26 1.59 some
# 1.0 1.59 2.01 people
# 1.0 2.04 2.220728 have
# 0.965297 2.220728 2.64 already
# 1.0 3.12 3.75 committed
# 1.0 3.81 3.93 to
# 1.0 3.93 4.44 memory
# 1.0 4.86 5.13 but
# 1.0 5.16 5.34 if
# 1.0 5.34 5.43 you
# 1.0 5.43 5.91 haven't
# 1.0 5.94 6.09 you
# 0.74926 6.09 6.39 shouldn't
# 1.0 6.39 6.81 before
# 1.0 6.81 7.05 your
# 1.0 7.14 7.77 interview
=== middle confidence: 0.9821598125 

# 1.0 8.91 8.97 the
# 1.0 8.97 9.27 table
# 1.0 9.27 9.66 comes
# 1.0 9.66 9.81 in
# 1.0 9.81 10.2 handy
# 1.0 10.23 10.77 often
# 1.0 11.22 11.4 in
# 1.0 11.4 12.0 scalability
# 1.0 12.0 12.51 question
# 0.967827 12.51 12.66 in
# 0.795548 12.66 13.05 computer
# 1.0 13.08 13.26 how
# 1.0 13.26 13.59 much
# 1.0 13.59 14.01 space
# 1.0 14.1 14.19 a
# 1.0 14.19 14.49 set
# 1.0 14.49 14.64 of
# 1.0 14.64 15.12 data
# 1.0 15.36 15.54 will
# 1.0 15.54 15.84 take
# 1.0 15.84 16.14 up
=== middle confidence: 0.9887321428571428 

["some people have already committed to memory but if you haven't you shouldn't before your interview", 'the table comes in handy often in scalability question in computer how much space a set of data will take up']
```
#### File format
It should be a Mono audio file, with Sample rate, the same as set in docker-compose.yml  
To prepare audio file we can use this command:
```
ffmpeg -i audio.wav -ac 1 -ar 16000 audio_prepared.wav
```
#### Based on
[sskorol's repo](https://github.com/sskorol/vosk-api-gpu) and his [docker image](https://hub.docker.com/r/sskorol/vosk-api/tags)