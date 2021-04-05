import logging
from resources.lib.tracker import Tracker

import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))

class AutoStreamSelectPlayer(xbmc.Player):

    def __init__(self, tracker:Tracker):
        logger.debug("--> PlayerInit")
        xbmc.Player.__init__(self)
        self._tracker = tracker
        # For the case when enabling the addon when something is already playing
        if xbmc.Player().isPlayingVideo():
            self._tracker.start()

    def onAVStarted(self):
        logger.warning("--> onAVStarted")
        logger.warning(xbmc.Player().isPlayingVideo())
        self._tracker.start()
        # xbmc.getInfoLabel('infolabel').
        # item_info = get_item_info()
        # if item_info and item_info["type"] == "episode":
        #     # Get identifiers
        #     tv_show_id = item_info["tvshowid"]
        #     showtitle = item_info["showtitle"]
        #     season = item_info["season"]
        #     episode = item_info["season"]

        #     # Get audio info, item info is not good enough
        #     properties = get_properties()
        #     audio_stream = properties["currentaudiostream"]
        #     audio_stream_index = properties["currentaudiostream"]["index"]
        #     audio_stream_name = properties["currentaudiostream"]["name"]


    def onAVChange(self):
        logger.warning("--> onAVChange")

    def onPlayBackStarted(self):
        logger.warning("--> onPlayBackStarted")

    def onPlayBackEnded(self):
        logger.warning("--> onPlayBackEnded")

    def onPlayBackStopped(self):
        logger.warning("--> onPlayBackStopped")
        self._tracker.stop()

    def onPlayBackPaused(self):
        logger.warning("--> onPlayBackPaused")

    def onPlayBackResumed(self):
        logger.warning("--> onPlayBackResumed")

    def onPlayBackSeek(self):
        logger.warning("--> onPlayBackSeek")

    def onPlayBackSeekChapter(self):
        logger.warning("--> onPlayBackSeekChapter")
