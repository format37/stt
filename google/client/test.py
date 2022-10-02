"""
This program sends audio file to the Flask server
over POST request
"""

import requests

url = 'http://127.0.0.1:4202/inference'
file_path = 'telegram.ogg'

with open(file_path, 'rb') as f:
    r = requests.post(url, files={'file': f})
    print(r.text)
