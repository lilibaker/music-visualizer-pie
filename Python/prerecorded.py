import itertools
import numpy as np
from scipy.io import wavfile
import serial
import sys
from pprint import pprint

BAUD = 9600

def draw(Ri, Ro, q, tmax=100, tstep=1):
    p = (Ro - Ri) / 2
    q = (Ro - p) * q + p
    R = Ri + p + q

    x = lambda t: (R - q)*np.cos(t) + p*np.cos(t*(R - q)/q)
    y = lambda t: (R - q)*np.sin(t) - p*np.sin(t*(R - q)/q)

    for t in range(0, tmax, tstep):
        yield {'x': x(t), 'y': y(t)}

if __name__ == "__main__":
    try:
        port, audiofile = sys.argv[1:3]
    except ValueError:
        print("Error: Use like python microphone.py PORT WAV_FILE")
        sys.exit(1)

    sr, data = wavfile.read(audiofile)
    parts = np.split(data - np.min(data), 3)

    avg = np.mean(parts, 1)
    avg = list(np.cumsum(avg / np.sum(avg)))

    pts = []
    for (Ri, Ro), part in zip(itertools.pairwise([0] + avg), parts):
        fqs = np.fft.rfftfreq(part.size, d=1./sr)
        dft = np.fft.rfft(part)
        dft = dft[(25 <= fqs) & (fqs <= 2000)]

        fq = fqs[np.argmax(dft)]
        q  = fq / 2000
        pts.extend(list(draw(Ro, Ri, q)))

    with serial.Serial(port, BAUD) as ser:
        for pt in pts:
            ser.write(f"{round(pt['x'], 2)},{round(pt['y'], 2)}".encode())