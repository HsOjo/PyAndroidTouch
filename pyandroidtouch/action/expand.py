import math as pymath

from pyandroidtouch.base import AndroidTouch
from pyandroidtouch.utils import math


@AndroidTouch.action
def expand(touch: AndroidTouch, ox, oy, size=128, distance=32, time=100, degree=0):
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
    pat = AndroidTouch(debug=True)
    expand(pat, 640, 360, time=300, degree=-45)
    expand(pat, 640, 360, distance=256, size=-128, time=300, degree=-45)
    pat.execute()
