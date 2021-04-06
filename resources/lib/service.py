# -*- coding: utf-8 -*-

import json
import logging
import os
from resources.lib.periodic_updater import PeriodicUpdater
from typing import Any, Dict, Tuple

import xbmc
import xbmcaddon
import xbmcvfs

from .kodi_rpc import do_rpc

from .player import SaasbopsPlayer
from .storage import Storage
from .tracker import Tracker

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo("id")

logger = logging.getLogger(ADDON_ID)


def run():
    storage_path = os.path.join(xbmcvfs.translatePath("special://profile"), "addon_data", ADDON_ID)
    data_filename = os.path.join(storage_path, "data.json")

    logger.debug("Data filename: %s", data_filename)
    os.makedirs(storage_path, exist_ok=True)

    def load():
        try:
            with open(data_filename) as data_file:
                data = json.load(data_file)
                logger.debug("Read data from: %s", data_filename)
                return data
        except:
            logger.debug("Data file %s did not exist return empty dict", data_filename)
            return {}

    def persist(data):
        try:
            with open(data_filename, 'w') as data_file:
                logger.debug(data)
                json.dump(data, data_file, indent=2)
                logger.debug("Written: %s", data_filename)
        except Exception as e:
            logger.exception(e)
            logger.error("Failed writing data file: %s", data_filename)
    storage = Storage(load, persist)

    periodic_updater = PeriodicUpdater(1, None)
    tracker = Tracker(periodic_updater, storage)
    player = SaasbopsPlayer(tracker)

    # 2 way dependency between tracker and player :(
    def set_audio_stream(stream):
        player.setAudioStream(stream)

    def set_subtitle_stream(enabled, stream):
        player.showSubtitles = enabled
        if enabled:
            player.setSubtitleStream(stream)

    tracker.set_audio_stream = set_audio_stream
    tracker.set_subtitle_stream = set_subtitle_stream

    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        # Sleep/wait for abort
        if monitor.waitForAbort(1):
            # Abort was requested while waiting. We should exit
            break
        # Interval is determined by the waitForAbort timeout
        periodic_updater.tick()
