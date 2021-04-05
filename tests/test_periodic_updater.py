import os
import sys
import time
import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from resources.lib.periodic_updater import PeriodicUpdater

def test_init():
    p = PeriodicUpdater(1, None)

def test_start_single():

    callback  = mock.Mock()

    p = PeriodicUpdater(0.5, callback)
    p.start()
    p.tick() # Gets ignored because too fast
    assert(callback.call_count == 0)
    time.sleep(0.6)
    p.tick() # Period passed, callback called
    assert(callback.call_count == 1)

def test_start_multiple():

    callback  = mock.Mock()

    p = PeriodicUpdater(0.5, callback)
    p.start()
    time.sleep(0.3)
    p.start()
    time.sleep(0.3)
    p.tick() # Gets ignored because second start call restarted the period
    assert(callback.call_count == 0)
    time.sleep(0.3)
    p.tick() # Period passed, callback called
    assert(callback.call_count == 1)


def test_stop():

    callback  = mock.Mock()

    p = PeriodicUpdater(0.5, callback)
    p.stop() # Should not cause problems
    p.start()
    p.stop()
    time.sleep(0.6)
    p.tick() # Gets ignored because not running
    assert(callback.call_count == 0)

