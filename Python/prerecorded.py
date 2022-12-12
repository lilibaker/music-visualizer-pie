import math
import numpy as np

def norm(v):
    """
    Calculate Euclidean norm of a vector
    """
    return math.sqrt(sum(e**2 for e in v))

def draw(Ri, Ro, q, tmax=100, N=100):
    """
    Return the points for a single Spirograph with inner radius Ri and outer
    radius Ro. q determines the complexity of the pattern (in a somewhat
    unpredictble manner). tmax is the upper-bound of the curve parameter,
    and N is the number of points to generate within this range.

    A tuple is returned where the first element is the X points and the second
    is the Y points, both lists.
    """
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
