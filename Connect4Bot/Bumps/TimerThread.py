import threading


class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._timer = threading.Timer(self._timeout, self._callback)

    def start(self):
        self._timer.start()

    def reset(self, timeout=None):
        if timeout:
            self._timeout = timeout
        self._timer.cancel()
        self._timer = threading.Timer(self._timeout, self._callback)
        self._timer.start()
