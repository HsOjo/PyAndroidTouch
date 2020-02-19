import json
import urllib.request


class AndroidTouch:
    _protected_fields = [
        '_pressure',
        '_auto_commit',
    ]

    def __init__(self, host='127.0.0.1', port=8080, debug=False):
        self._host = host
        self._port = port
        self._commands = []
        self._pressure = 50
        self._auto_commit = True
        self._auto_execute = True
        self._debug = debug
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

    def _point_event(self, type, x, y, contact, pressure):
        if pressure is None:
            pressure = self._pressure
        return dict(
            type=type,
            x=int(x), y=int(y),
            contact=int(contact),
            pressure=int(pressure)
        )

    def set_auto_commit(self, b: bool):
        self._auto_commit = b

    def set_auto_execute(self, b: bool):
        self._auto_execute = b

    def set_default_pressure(self, value: int):
        self._pressure = value

    def down(self, x, y, contact=0, pressure=None):
        return self._append(self._point_event('down', int(x), int(y), contact, pressure))

    def move(self, x, y, contact=0, pressure=None):
        return self._append(self._point_event('move', int(x), int(y), contact, pressure))

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
        if self._auto_commit and len(self._commands) > 0:
            if self._commands[-1]['type'] != 'commit':
                self.commit()
        if self._debug:
            for command in self._commands:
                print(command)
        url = 'http://%s:%s' % (self._host, self._port)
        data = json.dumps(self._commands).encode()
        urllib.request.urlopen(url, data)
        if clear:
            self._commands.clear()

    @staticmethod
    def action(func):
        # This is action decorator.
        def wraper(touch: AndroidTouch, *args, **kwargs):
            protect = {k: getattr(touch, k) for k in AndroidTouch._protected_fields}
            result = func(touch, *args, **kwargs)
            for k, v in protect.items():
                setattr(touch, k, v)
            if touch._auto_execute:
                touch.execute()
            return result

        return wraper
