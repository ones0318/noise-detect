import datetime
import logging
import sys
import time
import queue

import sounddevice as sd
import soundfile as sf
import numpy as np


q = queue.Queue(maxsize=512)

record = False
start = time.time()


logging.basicConfig(
    filename=f'{datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}.log',
    level=logging.INFO,
    format='%(asctime)s|%(name)s|%(levelname)s|%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def print_sound(indata, outdata, frames, time_, status):
    volume_norm = np.linalg.norm(indata)*10
    if q.full():
        q.get()
    q.put(indata.copy())

    global record
    global start

    threshold = 2
    if volume_norm > threshold and not record:
        start = time.time()
        logging.info(f'detect so   und!! threshold={threshold}')
        print('!!!detect!!!')
        record = True
    if record:
        if time.time() - start > 5:
            with sf.SoundFile(f'records/{datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}.wav', mode='w', samplerate=44100, channels=2) as fd:
                while not q.empty():
                    fd.write(q.get())
            record = False
    print("|" * int(volume_norm))


if __name__ == '__main__':
    time.sleep(900)
    with sd.Stream(callback=print_sound, blocksize=1024):
        sd.sleep(6*3600*1000)
