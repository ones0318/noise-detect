import datetime
import logging
import time
import queue

import sounddevice as sd
import soundfile as sf
import numpy as np


q = queue.Queue(maxsize=1*1024*1024)

record = False
start = time.time()

logging.basicConfig(
    filename=f'{datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def print_sound(indata, outdata, frames, time_, status):
    volume_norm = np.linalg.norm(indata)*10
    q.put(indata.copy())

    global record
    global start

    threshold = 1
    if volume_norm > threshold and not record:
        start = time.time()
        logging.info(f'detect sound!! threshold={threshold}')
        record = True
    if record:
        if time.time() - start > 10:
            with sf.SoundFile(f'records/{datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}.wav', mode='w', samplerate=44100, channels=2) as fd:
                while not q.empty():
                    fd.write(q.get())
            record = False
    print("|" * int(volume_norm))


with sd.Stream(callback=print_sound):
    sd.sleep(900*1000)
