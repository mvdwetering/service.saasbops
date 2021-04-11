import os
import sys
import mock
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from resources.lib.preferences import Preferences

class PreferencesTest(unittest.TestCase):

    def setUp(self):
        self.info = { "a": "b"}
        self.initial_preference_data = {
            "1" : {
                "2": {
                    "3": self.info
                }
            }
        }

        self.load  = mock.Mock()
        self.load.return_value = self.initial_preference_data

        self.persist  = mock.Mock()

    def test_init(self):
        p = Preferences(None, None)
        p = Preferences(self.load, None)
        assert(self.load.call_count == 1)


    def test_persist(self):
        test_info = { "a": 4 }

        p = Preferences(self.load, self.persist)
        p.set(1, 2, 3, test_info)

        persisted_data = {
            "1" : {
                "2": {
                    "3": test_info
                }
            }
        }
        self.persist.assert_called_with(persisted_data)
        assert(self.persist.call_count == 1)

    def test_set(self):
        test_info = {"c": "d"}

        p = Preferences(None, None)
        p.set(1, 2, 3, test_info)
        result = p.get(1, 2, 3)
        assert(test_info ==  result)


    def test_get_no_info(self):
        p = Preferences(self.load, None)

        # Show does not exist
        assert(None == p.get(123, 2, 3))
        # No earlier season
        assert(None == p.get(1, 1, 3))
        # No earlier episode
        assert(None == p.get(1, 2, 2))

    def test_get_find_earlier_info(self):
        p = Preferences(self.load, None)

        assert(self.info == p.get(1, 2, 4))
        assert(self.info == p.get(1, 3, 3))

