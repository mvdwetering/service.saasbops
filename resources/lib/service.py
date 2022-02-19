import json
import logging
import os
from resources.lib.periodic_updater import PeriodicUpdater
from typing import Any, Dict

import xbmc
import xbmcaddon

from .kodi_rpc import do_rpc

from .player import SaasbopsPlayer
from .preferences import Preferences
from .tracker import Tracker
from .common import get_storage_path, get_preferences_filename

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo("id")

logger = logging.getLogger(ADDON_ID)


def run():
    storage_path = get_storage_path()
    data_filename = get_preferences_filename()

    logger.debug("Data filename: %s", data_filename)
    os.makedirs(storage_path, exist_ok=True)

    def load():
        try:
            with open(data_filename) as data_file:
                data = json.load(data_file)
                logger.debug("Read data from: %s", data_filename)
                return data
        except:
            logger.debug(
                "Data file %s did not exist return empty dict", data_filename)
            return {}

    def save(data):
        try:
            with open(data_filename, 'w') as data_file:
                logger.debug(data)
                json.dump(data, data_file, indent=2)
                logger.debug("Written: %s", data_filename)
        except Exception as e:
            logger.exception(e)
            logger.error("Failed writing data file: %s", data_filename)

    preferences = Preferences(load, save)
    periodic_updater = PeriodicUpdater(1, None)
    tracker = Tracker(periodic_updater, preferences)
    player = SaasbopsPlayer(tracker)

    # 2 way dependency between tracker and player :(
    def set_audio_stream(stream):
        player.setAudioStream(stream)

    def set_subtitle_stream(enabled, stream):
        player.showSubtitles = enabled
        if enabled:
            player.setSubtitleStream(stream)
        # For some reason subtitle changes take a while to start working
        # Since this should happen only at the beginning of an episode
        # just go back to the beginning and they will work "instantly"
        player.seekTime(0)

    tracker.set_audio_stream = set_audio_stream
    tracker.set_subtitle_stream = set_subtitle_stream

    monitor = xbmc.Monitor()
    did_exist = os.path.exists(data_filename)

    while not monitor.abortRequested():
        if monitor.waitForAbort(1):
            # Abort was requested while waiting. We should exit
            break
        periodic_updater.tick()

        # Bit if a hack to clear the prefences when the datafile
        # is deleted by the script command
        exists = os.path.exists(data_filename)
        if did_exist and not exists:
            preferences.reset()
        did_exist = exists
