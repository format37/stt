#!/usr/bin/env python3

import asyncio
import websockets
import sys
import wave
import json

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
            if len(accept)>1 and accept['text'] != '':
                accept_text = str(accept['text'])                
                phrases.append(accept_text)						

        await websocket.send('{"eof" : 1}')
        accept = json.loads(await websocket.recv())					
        if len(accept)>1 and accept['text'] != '':
            accept_text = str(accept['text'])                
            phrases.append(accept_text)						

        print(phrases)

asyncio.run(run_test('ws://localhost:2700'))
