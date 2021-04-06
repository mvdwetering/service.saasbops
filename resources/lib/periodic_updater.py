import time

def _update():
    print("Update")

class PeriodicUpdater():
    """
    Periodically calls the given update_function.
    Simple implementation, not accurate at all!
    """

    def __init__ (self, period, callback):
        self.period = period
        self._callback = callback
        self._last_update = time.time()
        self._running = False

    def tick(self):
        if not self._running:
            return
        now = time.time()
        if now > self._last_update + self.period:
            self._last_update = now
            self._callback()

    def start(self):
        """(re)start periodic updates"""
        # Restart period when (re)starting
        self._last_update = time.time()
        self._running = True

    def stop(self):
        self._running = False

