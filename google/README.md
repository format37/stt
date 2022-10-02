# Google speech to text docker server
#### Installation
```
git clone https://github.com/format37/google_stt.git
cd google_stt
```
1. Create google cloud service account  
2. Download json key and put to server/api.json
```
sh compose
```
#### Using
```
cd client
python test.py
```
#### Expected output:
```
hi this is a test how you doing
```