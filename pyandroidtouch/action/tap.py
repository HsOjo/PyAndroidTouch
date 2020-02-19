from pyandroidtouch.base import AndroidTouch


@AndroidTouch.action
def tap(touch: AndroidTouch, x, y, press_time=100, count=1, delay_time=100,
        finger=1, finger_distance=64, finger_is_vertical=False, finger_offset=None):
    for n in range(count):
        if n > 0:
            touch.delay(delay_time)
        if finger > 1:
            length = (finger - 1) * finger_distance
            if finger_offset is None:
                finger_offset = (length / 2)
            for i in range(finger):
                if finger_is_vertical:
                    touch.down(x, y - finger_offset + finger_distance * i, i)
                else:
                    touch.down(x - finger_offset + finger_distance * i, y, i)
            touch.delay(press_time)
            for i in range(finger):
                touch.up(i)
        else:
            touch.down(x, y)
            touch.delay(press_time)
            touch.up()


if __name__ == '__main__':
    pat = AndroidTouch(debug=True)
    tap(pat, 360, 360, finger=3, count=2)
    pat.execute()
