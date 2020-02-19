import math as pymath

from pyandroidtouch.base import AndroidTouch
from pyandroidtouch.utils import math


@AndroidTouch.action
def circle(touch: AndroidTouch, ox, oy, radius=64, time=100, press_time=0, start_degree=0, count: float = 1,
           reverse=False, finger=1):
    length = 360
    distance = length * count
    step = distance / time
    count_step = int(distance // step)

    def calc_pos(degree):
        return math.move(ox, oy, radius, pymath.radians(degree))

    if finger > 1:
        finger_distance = length / finger
        for n in range(finger):
            touch.down(*calc_pos(start_degree), n)
        touch.delay(press_time)
        for i in range(1, count_step):
            d = i * step
            if reverse:
                d = -d
            for n in range(finger):
                touch.move(*calc_pos(start_degree + d - (finger_distance * n)), contact=n)
            touch.delay()
        for n in range(finger):
            touch.up(n)
    else:
        touch.down(*calc_pos(start_degree))
        touch.delay(press_time)
        for i in range(1, count_step):
            d = i * step
            if reverse:
                d = -d
            touch.move(*calc_pos(start_degree + d))
            touch.delay()
        touch.up()


if __name__ == '__main__':
    pat = AndroidTouch(debug=True)
    circle(pat, 640, 360, finger=1, time=500, count=1)
    circle(pat, 640, 360, finger=2, time=500, count=0.5)
