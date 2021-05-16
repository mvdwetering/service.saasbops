import os
import sys
import unittest
from unittest.mock import Mock

# This line needs to be _before_ referencing resources.lib.*
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # nopep8

from resources.lib.tracker import find_audio_stream, same_subtitle


class TrackerTest(unittest.TestCase):

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

        self.persist = Mock()

    def test_find_audio_stream(self):
        requested = {'bitrate': 0, 'channels': 2, 'codec': 'aac', 'index': 0, 'isdefault': False,
                     'isimpaired': False, 'isoriginal': False, 'language': 'jpn', 'name': 'AAC stereo', 'samplerate': 0}
        audio_streams = [{'bitrate': 0, 'channels': 2, 'codec': 'aac', 'index': 0, 'isdefault': True, 'isimpaired': False, 'isoriginal': False, 'language': 'eng', 'name': 'Golumpa@FUNI - AAC stereo',
                          'samplerate': 0}, {'bitrate': 0, 'channels': 2, 'codec': 'aac', 'index': 1, 'isdefault': False, 'isimpaired': False, 'isoriginal': False, 'language': 'jpn', 'name': 'AAC stereo', 'samplerate': 0}]

        stream = find_audio_stream(requested, audio_streams)
        assert(stream == 1)

    def test_same_subtitle(self):
        sub1 = {
            "index": 0,
            "isdefault": True,
            "isforced": False,
            "isimpaired": False,
            "language": "eng",
            "name": "Track 1"
        }
        sub2 = sub1.copy()

        # Handle None (disabled) subtitle
        self.assertTrue(same_subtitle(None, None))
        self.assertFalse(same_subtitle(sub1, None))
        self.assertFalse(same_subtitle(None, sub1))

        # Don't care items
        self.assertTrue(same_subtitle(sub1, sub2))
        sub2["index"] = 1
        self.assertTrue(same_subtitle(sub1, sub2))
        sub2 = sub1.copy()
        sub2["isdefault"] = False
        self.assertTrue(same_subtitle(sub1, sub2))

        # Items that cause differences
        sub2 = sub1.copy()
        sub2["isforced"] = True
        self.assertFalse(same_subtitle(sub1, sub2))
        sub2 = sub1.copy()
        sub2["isimpaired"] = True
        self.assertFalse(same_subtitle(sub1, sub2))
        sub2 = sub1.copy()
        sub2["language"] = "not eng"
        self.assertFalse(same_subtitle(sub1, sub2))
        sub2 = sub1.copy()
        sub2["name"] = "Track 2"
        self.assertFalse(same_subtitle(sub1, sub2))
