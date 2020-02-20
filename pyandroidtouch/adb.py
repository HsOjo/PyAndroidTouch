import os
import time
from threading import Thread

from pyadb import Device, PyADB

from pyandroidtouch import common
from pyandroidtouch.py import PyAndroidTouch


class PyAndroidTouchADB(PyAndroidTouch):
    PATH_REMOTE = '/data/local/tmp/android_touch'

    def __init__(self, device: Device, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._device = device

        abi = device.abi
        path_touch = common.get_module_res('libs/%s/android_touch' % abi)
        if os.path.exists(path_touch):
            self.print_debug('Pushing "android_touch".')
            if device.file.push(path_touch, remote=self.PATH_REMOTE):
                device.execute('chmod', '+x', self.PATH_REMOTE)
                f = device.forward
                port = None
                for p in range(50000, 65535):
                    if f.tcp(p, 8080):
                        port = p
                        break

                self.set_device(port=port)
                self.print_debug('Forward Port: %s' % port)
                self.print_debug('Current Forward Ports: ', *['\n\t%a' % i for i in f.list])
            else:
                raise Exception('Push File Failed!', device.adb.last_exec)
        else:
            raise FileNotFoundError('Unsupport ABI: %s.' % abi)

        self.print_debug('Waiting "android_touch" init.')

        self._t = Thread(target=self._t_init)
        self._t.start()

        while self.pid is None:
            time.sleep(0.1)

        self.print_debug('Init Success.')

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
        self._device.file.delete(self.PATH_REMOTE)
        self._device.forward.remove('tcp:%s' % self._port)
        self.print_debug('Destroy Finish.')


if __name__ == '__main__':
    adb = PyADB()
    device = list(adb.devices.values())[0]
    pat = PyAndroidTouchADB(device, debug=True)
    pat.tap(640, 360, finger=2, finger_degree=45)
    pat.tap(100, 200).wait(500).tap(200, 300).execute()
    pat.destroy()
