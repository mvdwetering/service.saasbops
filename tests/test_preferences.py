import sys
import os
import unittest
from unittest.mock import Mock

# This line needs to be _before_ referencing resources.lib.*
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # nopep8

from resources.lib.preferences import Preferences


class PreferencesTest(unittest.TestCase):

    def setUp(self):
        self.info = {"a": "b"}
        self.initial_preference_data = {
            "1": {
                "2": {
                    "3": self.info
                }
            }
        }

        self.load = Mock()
        self.load.return_value = self.initial_preference_data

        self.save = Mock()

    def test_init(self):
        p = Preferences(None, None)
        p = Preferences(self.load, None)
        assert(self.load.call_count == 1)

    def test_save(self):
        test_info = {"a": 4}

        p = Preferences(self.load, self.save)
        p.set(1, 2, 3, test_info)

        persisted_data = {
            "1": {
                "2": {
                    "3": test_info
                }
            }
        }
        self.save.assert_called_with(persisted_data)
        assert(self.save.call_count == 1)

    def test_set(self):
        test_info = {"c": "d"}

        p = Preferences(None, None)
        p.set(1, 2, 3, test_info)
        result = p.get(1, 2, 3)
        assert(test_info == result)

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
