import os
import tempfile
import time
from threading import Thread

from pyadb import Device, PyADB

from pyandroidtouch import common
from pyandroidtouch.py import PyAndroidTouch


class PyAndroidTouchADB(PyAndroidTouch):
    PATH_REMOTE = '/data/local/tmp/android_touch'

    def __init__(self, device: Device):
        self._device = device
        self._port = None

        abi = device.abi
        path_touch = common.get_module_res('libs/%s/android_touch' % abi)
        if os.path.exists(path_touch):
            if device.file.push(path_touch, remote=self.PATH_REMOTE):
                device.execute('chmod', '+x', self.PATH_REMOTE)
                f = device.forward
                port = None
                for p in range(50000, 65535):
                    if f.tcp(p, 8080):
                        port = p
                        break
            else:
                raise Exception('Push File Failed!', device.adb.last_exec)
        else:
            raise FileNotFoundError('Unsupport ABI: %s.' % abi)

        super().__init__(port=port)

        self._t = Thread(target=self._t_init)
        self._t.start()

        while self.pid is None:
            time.sleep(0.1)

    @property
    def pid(self):
        out = self._device.execute_out("ps|grep android_touch|awk '{ print $2 }'")
        if out != '':
            return int(out)
        else:
            return None

    def _t_init(self):
        self._device.execute("kill", '-9', self.pid)
        adb = self._device.adb.copy()
        adb.current_device.execute(self.PATH_REMOTE)

    def destroy(self):
        self._device.execute("kill", '-9', self.pid)
        f = self._device.forward
        if self._port is not None:
            f.remove('tcp:%s' % self._port)

    def __del__(self):
        self.destroy()


if __name__ == '__main__':
    adb = PyADB()
    device = list(adb.devices.values())[1]
    pat = PyAndroidTouchADB(device)
    pat.tap(640, 360)
    pat.destroy()
