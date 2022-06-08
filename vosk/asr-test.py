#!/usr/bin/env python3

import asyncio
import websockets
import sys
import wave
import json

def accept_feature_extractor(phrases, accept):    
    if len(accept)>1 and accept['text'] != '':        
        accept_text = str(accept['text'])                
        accept_start = str(accept['result'][0]['start'])
        accept_end = accept['result'][-1:][0]['end']        
        conf_score = []
        for result_rec in accept['result']:
            print('#', result_rec['conf'], result_rec['start'], result_rec['end'], result_rec['word'])
            conf_score.append(float(result_rec['conf']))
        conf_mid = str(sum(conf_score)/len(conf_score))
        print('=== middle confidence:', conf_mid, '\n')
        phrases.append(accept_text)

async def run_test(uri):

    phrases = []

    async with websockets.connect(uri) as websocket:

        wf = wave.open(sys.argv[1], "rb")        
        await websocket.send('{ "config" : { "sample_rate" : %d } }' % (wf.getframerate()))
        buffer_size = int(wf.getframerate() * 0.2) # 0.2 seconds of audio
        while True:
            data = wf.readframes(buffer_size)

            if len(data) == 0:
                break

            await websocket.send(data)
            accept = json.loads(await websocket.recv())					
            accept_feature_extractor(phrases, accept)

        await websocket.send('{"eof" : 1}')
        accept = json.loads(await websocket.recv())		
        accept_feature_extractor(phrases, accept)

        print(phrases)

asyncio.run(run_test('ws://localhost:2700'))
