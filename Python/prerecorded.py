import itertools
import math
import serial
import sys
from pprint import pprint
import numpy as np

BAUD = 9600
SCALE = 325 # 325 mm is the size of drawing area and steps are in mm

def norm(v):
    return math.sqrt(sum(e**2 for e in v))

def draw(Ri, Ro, q, tmax=100, N=1000):
    Ro, Ri = max(Ri, Ro), min(Ri, Ro)
    p = (Ro - Ri) / 2
    q = (Ro - p) * q + p
    R = Ri + p + q
    q = min(0.1, q)

    x = lambda t: (R - q)*math.cos(t) + p*math.cos(t*(R - q)/q)
    y = lambda t: (R - q)*math.sin(t) - p*math.sin(t*(R - q)/q)

    xs = [0] +  [x(t) for t in np.linspace(0, tmax, N)]
    ys = [0] +  [y(t) for t in np.linspace(0, tmax, N)]

    return xs, ys
