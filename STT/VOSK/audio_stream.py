import queue
import sounddevice as sd
from config import SAMPLE_RATE

q = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def start_stream(callback=audio_callback):
    return sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                             channels=1, callback=callback)
