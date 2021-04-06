import logging
from enum import Enum
from typing import Optional

import xbmcaddon

from .kodi_utils import get_item_info, get_properties
from .periodic_updater import PeriodicUpdater
from .storage import Storage

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))


def same_audio(audio1, audio2) -> bool:
    """Check if same audio, needed because other attributes can differ"""
    if (audio1['name'] == audio2['name'] and
        audio1['language'] == audio2['language'] and
        audio1['isimpaired'] == audio2['isimpaired'] ):
        return True
    return False

def same_subtitle(subtitle1, subtitle2) -> bool:
    """Check if same subtitle, needed because other attributes can be differ"""

    if subtitle1 == subtitle2:
        return True

    if subtitle1 is None or subtitle2 is None:
        return False

    if (subtitle1['name'] == subtitle2['name'] and
        subtitle1['language'] == subtitle2['language'] and
        subtitle1['isforced'] == subtitle2['isforced'] and
        subtitle1['isimpaired'] == subtitle2['isimpaired']):
        return True
    return False


def find_audio_stream(requested_audio, audio_streams) -> Optional[int]:
    for audio_stream in audio_streams:
        if same_audio(requested_audio, audio_stream):
            return audio_stream["index"]
    return None

def find_subtitle_stream(requested_subtitle, subtitles) -> Optional[int]:
    for subtitle in subtitles:
        if same_subtitle(requested_subtitle, subtitle):
            return subtitle["index"]
    return None


class State(Enum):
    STOPPED = 0
    PLAYING = 1


class Tracker():

    def __init__(self, periodic_updater: PeriodicUpdater, storage: Storage):
        logger.debug("--> Tracker Init")
        self.item = None
        self.type = None
        self.state = State.STOPPED
        self.storage = storage
        self.periodic_updater = periodic_updater
        periodic_updater._callback = self._update_item  # Hmmm
        self.audio = None
        self.subtitle = None
        self.set_audio_stream = None
        self.set_subtitle_stream = None

    def _reset(self):
        self.audio = None
        self.subtitle = None

    def _get_audio(self, properties):
        return properties["currentaudiostream"]

    def _get_subtitle(self, properties):
        if properties["subtitleenabled"] == False:
            return None
        sub = properties["currentsubtitle"]
        logger.debug(sub)
        return sub

    def _update_item(self, initial: bool = False):
        logger.debug("--> Update item")

        item_info = get_item_info()
        if item_info["type"] != "episode":
            logger.debug("Not an episode")
            return

        try:
            show_id = item_info["tvshowid"]
            season = item_info["season"]
            episode = item_info["episode"]

            logger.debug("show: %d, season:%d, episode:%d",
                         show_id, season, episode)

            item_props = get_properties()
            current_audio = self._get_audio(item_props)
            current_subtitle = self._get_subtitle(item_props)

            logger.debug(
                "audio: %d, %s, %s", current_audio["index"], current_audio["language"], current_audio["name"])
            logger.debug(
                "subtitle: %s", f'{current_subtitle["index"]}, {current_subtitle["language"]}, {current_subtitle["name"]}' if current_subtitle else "subtitles disabled")

            if initial:
                self.audio = current_audio
                self.subtitle = current_subtitle

                stored_info = self.storage.get_info(show_id, season, episode)
                logger.debug("Initial info: %s", stored_info)

                if stored_info is not None:
                    # Will match the stored settings
                    self.audio = stored_info["audio"]
                    self.subtitle = stored_info["subtitle"]

                    if not same_audio(stored_info["audio"], current_audio):
                        logger.info(
                            "Current audio is different from data audio -> Overriding audio")
                        logger.debug(stored_info["audio"])
                        logger.debug(item_props["audiostreams"])
                        stream = find_audio_stream(stored_info["audio"], item_props["audiostreams"])
                        if stream is not None and self.set_audio_stream:
                            logger.debug("Setting audiostream: %d, %s, %s", stream, stored_info["audio"]["language"], stored_info["audio"]["name"])
                            self.set_audio_stream(stream)
                    if not same_subtitle(stored_info["subtitle"], current_subtitle):
                        logger.info(
                            "Current subtitle is different from data subtitle -> Overriding subtitle")
                        logger.debug(stored_info["subtitle"])
                        logger.debug(item_props["subtitles"])
                        stream = find_subtitle_stream(stored_info["subtitle"], item_props["subtitles"])
                        logger.debug("Setting subtitlestream: %d, %s", stream, f'{stored_info["subtitle"]["language"]}, {stored_info["subtitle"]["name"]}' if stored_info["subtitle"] else "subtitles disabled")
                        enabled = stored_info["subtitle"] is not None
                        if stream is not None and self.set_subtitle_stream:
                            self.set_subtitle_stream(enabled, stream)

            if not initial:
                # Check for changes and store if different cause it is what the user specified
                if not same_audio(self.audio, current_audio) or not same_subtitle(self.subtitle, current_subtitle):
                    logger.debug("same_audio: %s\n    %s\n    %s", same_audio(self.audio, current_audio), self.audio, current_audio)
                    logger.debug("same_subtitle: %s\n    %s\n    %s", same_subtitle(self.subtitle, current_subtitle), self.subtitle, current_subtitle)
                    self.storage.set_info(show_id, season, episode, {
                                          "audio": current_audio, "subtitle": current_subtitle})

        except Exception as e:
            logger.error(e)

    def start(self):
        logger.debug("--> Start")
        self._reset()
        self.state = State.PLAYING
        self._update_item(initial=True)
        self.periodic_updater.start()

    def stop(self):
        logger.debug("--> Stop")
        self.periodic_updater.stop()
        self.state = State.STOPPED
