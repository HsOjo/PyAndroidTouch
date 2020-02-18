from pyandroidtouch import PyAndroidTouch


@PyAndroidTouch.action
def tap(touch: PyAndroidTouch, x, y, finger=1, finger_distance=64, finger_is_vertical=False, offset=None,
        press_time=100, count=1,
        delay_time=100):
    for n in range(count):
        if n > 0:
            touch.delay(delay_time)
        if finger > 1:
            length = (finger - 1) * finger_distance
            if offset is None:
                offset = (length / 2)
            for i in range(finger):
                if finger_is_vertical:
                    touch.down(x, y - offset + finger_distance * i, i)
                else:
                    touch.down(x - offset + finger_distance * i, y, i)
            touch.delay(press_time)
            for i in range(finger):
                touch.up(i)
        else:
            touch.down(x, y)
            touch.delay(press_time)
            touch.up()


if __name__ == '__main__':
    pat = PyAndroidTouch(debug=True)
    tap(pat, 360, 360, 3, count=2)
    pat.execute()
