from pyandroidtouch import action
from pyandroidtouch.base import AndroidTouch


class PyAndroidTouch(AndroidTouch):
    @staticmethod
    def _action(params: dict):
        params['touch'] = params.pop('self')
        return params

    def tap(self, x, y, press_time=100, count=1, delay_time=100,
            finger=1, finger_distance=64, finger_is_vertical=False, finger_offset=None):
        return action.tap(**self._action(locals()))

    def swipe(self, sx, sy, ex, ey, time=100,
              finger=1, finger_distance=64, finger_offset=None):
        return action.swipe(**self._action(locals()))

    def circle(self, ox, oy, radius=64, time=100, press_time=0, start_degree=0, count: float = 1,
               reverse=False, finger=1):
        return action.circle(**self._action(locals()))

    def expand(self, ox, oy, size=128, distance=32, time=100, degree=0):
        return action.expand(**self._action(locals()))


if __name__ == '__main__':
    PyAndroidTouch().tap(640, 360)
