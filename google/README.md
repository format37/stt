# Google speech to text docker server
#### Installation
```
git clone https://github.com/format37/stt.git
cd stt/google
```
1. Create google cloud service account  
2. Download json key and put to server/api.json
```
sh compose.sh
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