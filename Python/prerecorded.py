import itertools
import numpy as np
from scipy.io import wavfile
import serial
import sys
from pprint import pprint

BAUD = 9600

def draw(Ri, Ro, q, tmax=100, tstep=10):
    p = (Ro - Ri) / 2
    q = (Ro - p) * q + p
    R = Ri + p + q

    x = lambda t: (R - q)*np.cos(t) + p*np.cos(t*(R - q)/q)
    y = lambda t: (R - q)*np.sin(t) - p*np.sin(t*(R - q)/q)

    xs = np.array([x(t) for t in range(0, tmax, tstep)])
    ys = np.array([y(t) for t in range(0, tmax, tstep)])
    xs = list((xs - np.mean(xs)) / (10*np.std(xs)))
    ys = list((ys - np.mean(ys)) / (10*np.std(ys)))
    #xs = (xs - np.min(xs)) * 0.5 / (np.min(xs) + np.max(xs)) - 0.25
    #ys = (ys - np.min(ys)) * 0.5 / (np.min(ys) + np.max(ys)) - 0.25

    return xs, ys

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
    XS = []
    YS = []
    for (Ri, Ro), part in zip(itertools.pairwise([0] + avg), parts):
        fqs = np.fft.rfftfreq(part.size, d=1./sr)
        dft = np.fft.rfft(part)
        dft = dft[(25 <= fqs) & (fqs <= 2000)]

        fq = fqs[np.argmax(dft)]
        q  = fq / 2000
        #pts.extend(list(draw(Ro, Ri, q)))
        xs, ys = draw(Ro, Ri, q)
        XS = np.array(list(XS) + list(xs))#np.concatenate(XS, xs)
        YS = np.array(list(YS) + list(ys))#np.concatenate(YS, ys)

    str = ""
    for x, y in zip(XS, YS):
        str = str + f"{round(x, 2)},{round(y, 2)} "

    print(str)
    #pprint(XS)
    #port = sys.argv[1]
    #port = "COM9"
    #with serial.Serial(port, BAUD) as ser:
        #for x, y in zip(XS, YS):
        #    ser.write(f"{round(x, 2)},{round(y, 2)}\n".encode())
            #print(f"{round(x, 2)},{round(y, 2)}")

        #for i in range(61):
        #    ser.write(f"100,100\n".encode())
        #ser.write("0.03,0.03\n".encode())
        #for x, y in zip(XS, YS):
        #    ser.write(f"{round(x, 2)},{round(y, 2)}\n".encode())a
        #ser.write("100,100\n".encode())
        #ser.write("100,100\n".encode())
