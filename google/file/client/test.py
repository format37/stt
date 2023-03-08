"""
This program sends audio file to the Flask server
over POST request
"""

import requests

url = 'http://127.0.0.1:4212/inference'
file_path = 'telegram.ogg'

language_code = 'en'
"""if language_code == '':
    with open(file_path, 'rb') as f:
        r = requests.post(url, files={'file': f})
        print(r.text)
else:
"""    
with open(file_path, 'rb') as f:
    r = requests.post(url, files={'file': f}, data={'language_code': language_code})
    print(r.text)
