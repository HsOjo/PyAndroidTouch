import math as pymath

from pyandroidtouch import PyAndroidTouch
from pyandroidtouch.utils import math


@PyAndroidTouch.action
def circle(touch: PyAndroidTouch, ox, oy, finger=1, radius=64, time=100, start_degree=0, count=1, reverse=False):
    step = 360 / time
    count_step = int(360 // step)
    degree = start_degree

    if finger >1:
        length = (finger - 1) * 360

        def finger_action(down=False):
            for i in range(finger):
                fx, fy = math.move(x, y, -offset + finger_distance * i, angle - r90)
                if down:
                    touch.down(fx, fy, i)
                else:
                    touch.move(fx, fy, i)

    else:
        def calc_pos(degree):
            return math.move(ox, oy, radius, pymath.radians(degree))

        x, y = calc_pos(degree)
        for n in range(count):
            if n == 0:
                touch.down(x, y)
            for i in range(1, count_step):
                d = i * step
                if reverse:
                    d = -d
                x, y = calc_pos(degree + d)
                touch.move(x, y)
                touch.delay()
        touch.up()


if __name__ == '__main__':
    pat = PyAndroidTouch(debug=True)
    circle(pat, 640, 360, count=2, time=100)
    pat.execute()
