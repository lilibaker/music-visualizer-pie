import itertools
import math
from scipy.io import wavfile
import serial
import sys
from pprint import pprint

BAUD = 9600
SCALE = 32.33 # 32.33 mm is the size of drawing area and steps are in mm

def norm(v):
    return math.sqrt(sum(e**2 for e in v))

def draw(Ri, Ro, q, tmax=100, tstep=10):
    Ro, Ri = max(Ri, Ro), min(Ri, Ro)
    p = (Ro - Ri) / 2
    q = (Ro - p) * q + p
    R = Ri + p + q
    q = min(0.1, q)

    x = lambda t: (R - q)*math.cos(t) + p*math.cos(t*(R - q)/q)
    y = lambda t: (R - q)*math.sin(t) - p*math.sin(t*(R - q)/q)

    xs = [x(t) for t in range(0, tmax, tstep)]
    ys = [y(t) for t in range(0, tmax, tstep)]
    xs = [x / norm(xs) * SCALE for x in xs]
    ys = [y / norm(ys) * SCALE for y in ys]

    return xs, ys
