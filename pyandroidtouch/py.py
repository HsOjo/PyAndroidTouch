import math as pymath

from pyandroidtouch.base import AndroidTouch
from pyandroidtouch.utils import math


def _action(func):
    # This is _action decorator.
    def wraper(self: 'PyAndroidTouch', *args, **kwargs):
        protect = {k: getattr(self, k) for k in PyAndroidTouch._protected_fields}
        result = func(self, *args, **kwargs)
        for k, v in protect.items():
            setattr(self, k, v)
        if self._auto_execute:
            self.execute()
        return result

    return wraper


class PyAndroidTouch(AndroidTouch):
    _protected_fields = [
        '_pressure',
        '_auto_commit',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._auto_commit = True
        self._auto_execute = True
        self._pos = {}

    def _append(self, command):
        c_type = command['type']
        if c_type in ['down', 'move']:
            contact = command['contact']
            x, y = command['x'], command['y']
            pos = self._pos.get(contact)
            if pos is None or c_type == 'down':
                self._pos[contact] = x, y
            else:
                px, py = pos
                if px == x and py == y:
                    return False
                else:
                    self._pos[contact] = x, y

        if len(self._commands) > 0:
            prev = self._commands[-1]
            p_type = prev['type']
            if self._auto_commit and c_type != 'commit':
                if p_type not in ['commit', 'delay'] and p_type != c_type:
                    self.commit()

            if p_type == 'delay' and c_type == p_type == 'delay':
                prev['value'] += command['value']
                return False

        self._commands.append(command)
        return True

    def set_auto_commit(self, b: bool):
        self._auto_commit = b

    def set_auto_execute(self, b: bool):
        self._auto_execute = b

    def execute(self, clear=True):
        if self._auto_commit and len(self._commands) > 0:
            if self._commands[-1]['type'] != 'commit':
                self.commit()
        super().execute()

    @_action
    def wait(self, time: int):
        self.delay(time)
        return self

    @_action
    def tap(self, x, y, press_time=100, count=1, delay_time=100,
            finger=1, finger_distance=64, finger_degree=0, finger_offset=None):
        angle = pymath.radians(finger_degree)
        length = (finger - 1) * finger_distance
        if finger_offset is None:
            finger_offset = (length / 2)

        for n in range(count):
            if n > 0:
                self.delay(delay_time)
            if finger > 1:
                for i in range(finger):
                    self.down(*math.move(x, y, -finger_offset + finger_distance * i, angle), i)
                self.delay(press_time)
                for i in range(finger):
                    self.up(i)
            else:
                self.down(x, y)
                self.delay(press_time)
                self.up()

        return self

    @_action
    def swipe(self, sx, sy, ex, ey, press_time=0, time=100,
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
                        self.down(fx, fy, i)
                    else:
                        self.move(fx, fy, i)

            finger_action(True)
            self.delay(press_time)
            for i in range(1, count_step + 1):
                x, y = math.move(sx, sy, i * step, angle)
                finger_action()
                self.delay()
            x, y = ex, ey
            finger_action()
            for i in range(finger):
                self.up(i)
        else:
            x, y = sx, sy
            self.down(x, y)
            self.delay(press_time)
            for i in range(1, count_step + 1):
                x, y = math.move(sx, sy, i * step, angle)
                self.move(x, y)
                self.delay()
            self.move(ex, ey)
            self.up()

        return self

    @_action
    def circle(self, ox, oy, radius=64, time=100, press_time=0, start_degree=0, count: float = 1,
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
                self.down(*calc_pos(start_degree), n)
            self.delay(press_time)
            for i in range(1, count_step):
                d = i * step
                if reverse:
                    d = -d
                for n in range(finger):
                    self.move(*calc_pos(start_degree + d - (finger_distance * n)), contact=n)
                self.delay()
            for n in range(finger):
                self.up(n)
        else:
            self.down(*calc_pos(start_degree))
            self.delay(press_time)
            for i in range(1, count_step):
                d = i * step
                if reverse:
                    d = -d
                self.move(*calc_pos(start_degree + d))
                self.delay()
            self.up()

        return self

    @_action
    def expand(self, ox, oy, size=128, distance=32, time=100, degree=0):
        step = size / time
        count_step = int(size // step)
        angle = pymath.radians(degree)

        for i in range(2):
            self.down(ox, oy, i)

        m = {0: -1, 1: 1}
        for n in range(1, count_step + 1):
            for i in range(2):
                x, y = math.move(ox, oy, m[i] * (n * step + distance), angle)
                self.move(x, y, i)
            self.delay()

        for i in range(2):
            self.up(i)

        return self


if __name__ == '__main__':
    PyAndroidTouch().tap(640, 360)
