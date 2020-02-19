import os
import tempfile


def get_module_res(res, bin=False):
    try:
        from pkg_resources import resource_stream
        data = resource_stream(__name__, os.path.join(res)).read()
        if bin:
            return data
        else:
            path = tempfile.mktemp()
            with open(path, 'bw') as io:
                io.write(data)
            return path
    except ImportError:
        path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__), *res))
        if bin:
            with open(path, 'br') as io:
                return io.read()
        return path
