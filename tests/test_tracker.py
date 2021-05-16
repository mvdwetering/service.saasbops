import os
import sys
import unittest
from unittest.mock import Mock

# This line needs to be _before_ referencing resources.lib.*
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # nopep8

from resources.lib.tracker import find_audio_stream


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
