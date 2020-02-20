import json
import urllib.request


class AndroidTouch:
    def __init__(self, debug=False):
        self._host = '127.0.0.1'
        self._port = 8080
        self._pressure = 50
        self._commands = []
        self._debug = debug

    def _append(self, command):
        self._commands.append(command)
        return True

    def _point_event(self, type, x, y, contact, pressure):
        if pressure is None:
            pressure = self._pressure
        return dict(
            type=type,
            x=int(x), y=int(y),
            contact=int(contact),
            pressure=int(pressure)
        )

    def set_device(self, host='127.0.0.1', port=8080):
        self._host = host
        self._port = port

    def set_default_pressure(self, value: int):
        self._pressure = value

    def down(self, x, y, contact=0, pressure=None):
        return self._append(self._point_event('down', x, y, contact, pressure))

    def move(self, x, y, contact=0, pressure=None):
        return self._append(self._point_event('move', x, y, contact, pressure))

    def up(self, contact=0):
        return self._append(dict(type='up', contact=contact))

    def delay(self, value=1):
        if value > 0:
            return self._append(dict(type='delay', value=value))
        else:
            return False

    def commit(self):
        return self._append(dict(type='commit'))

    def execute(self, clear=True):
        try:
            for command in self._commands:
                self.print_debug(command)
            url = 'http://%s:%s' % (self._host, self._port)
            data = json.dumps(self._commands).encode()
            urllib.request.urlopen(url, data)
            if clear:
                self._commands.clear()
            return True
        except:
            return False

    def print_debug(self, *args, **kwargs):
        if self._debug:
            print('[%s]' % self.__class__.__name__, *args, **kwargs)
