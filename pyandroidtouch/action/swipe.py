import math as pymath

from pyandroidtouch.base import AndroidTouch
from pyandroidtouch.utils import math


@AndroidTouch.action
def swipe(touch: AndroidTouch, sx, sy, ex, ey, time=100,
          finger=1, finger_distance=64, finger_offset=None):
    distance = math.distance(sx, sy, ex, ey)
    step = distance / time
    count_step = int(distance // step)
    angle = math.angle(sx, sy, ex, ey)
    r90 = pymath.radians(90)

    if finger > 1:
        length = (finger - 1) * finger_distance
        if finger_offset is None:
            finger_offset = (length / 2)

        x, y = sx, sy

        def finger_action(down=False):
            for i in range(finger):
                fx, fy = math.move(x, y, -finger_offset + finger_distance * i, angle - r90)
                if down:
                    touch.down(fx, fy, i)
                else:
                    touch.move(fx, fy, i)

        finger_action(True)
        for i in range(1, count_step + 1):
            x, y = math.move(sx, sy, i * step, angle)
            finger_action()
            touch.delay()
        x, y = ex, ey
        finger_action()
        for i in range(finger):
            touch.up(i)
    else:
        x, y = sx, sy
        touch.down(x, y)
        for i in range(1, count_step + 1):
            x, y = math.move(sx, sy, i * step, angle)
            touch.move(x, y)
            touch.delay()
        touch.move(ex, ey)
        touch.up()


if __name__ == '__main__':
    pat = AndroidTouch(debug=True)
    swipe(pat, 640, 0, 640, 720, time=100, finger=2)
    pat.execute()
