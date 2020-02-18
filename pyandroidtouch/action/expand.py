import math as pymath

from pyandroidtouch import PyAndroidTouch
from pyandroidtouch.utils import math


@PyAndroidTouch.action
def expand(touch: PyAndroidTouch, ox, oy, distance=32, size=128, time=100, degree=0):
    step = size / time
    count_step = int(size // step)
    angle = pymath.radians(degree)

    for i in range(2):
        touch.down(ox, oy, i)

    m = {0: -1, 1: 1}
    for n in range(1, count_step + 1):
        for i in range(2):
            x, y = math.move(ox, oy, m[i] * (n * step + distance), angle)
            touch.move(x, y, i)
        touch.delay()

    for i in range(2):
        touch.up(i)


if __name__ == '__main__':
    pat = PyAndroidTouch(debug=True)
    expand(pat, 640, 360, time=300, degree=-45)
    pat.execute()
