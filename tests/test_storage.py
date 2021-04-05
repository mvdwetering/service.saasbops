import os
import sys
import mock
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from resources.lib.storage import Storage

class StorageTest(unittest.TestCase):

    def setUp(self):
        self.info = { "a": "b"}
        self.initial_storage_data = {
            "1" : {
                "2": {
                    "3": self.info
                }
            }
        }

        self.load  = mock.Mock()
        self.load.return_value = self.initial_storage_data

        self.persist  = mock.Mock()

    def test_init(self):
        s = Storage(None, None)
        s = Storage(self.load, None)
        assert(self.load.call_count == 1)


    def test_persist(self):
        test_info = { "a": 4 }

        s = Storage(self.load, self.persist)
        s.set_info(1, 2, 3, test_info)

        persisted_data = {
            "1" : {
                "2": {
                    "3": test_info
                }
            }
        }
        self.persist.assert_called_with(persisted_data)
        assert(self.persist.call_count == 1)

    def test_set_info(self):
        test_info = {"c": "d"}

        s = Storage(None, None)
        s.set_info(1, 2, 3, test_info)
        result = s.get_info(1, 2, 3)
        assert(test_info ==  result)


    def test_get_info_no_info(self):
        s = Storage(self.load, None)

        # Show does not exist
        assert(None == s.get_info(123, 2, 3))
        # No earlier season
        assert(None == s.get_info(1, 1, 3))
        # No earlier episode
        assert(None == s.get_info(1, 2, 2))

    def test_get_info_find_earlier_info(self):
        s = Storage(self.load, None)

        assert(self.info == s.get_info(1, 2, 4))
        assert(self.info == s.get_info(1, 3, 3))

