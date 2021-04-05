import logging
from resources.lib.tracker import Tracker

import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))

class SaasbopsPlayer(xbmc.Player):

    def __init__(self, tracker:Tracker):
        logger.debug("--> PlayerInit")
        xbmc.Player.__init__(self)
        self._tracker = tracker
        # For the case when enabling the addon when something is already playing
        if xbmc.Player().isPlayingVideo():
            self._tracker.start()

    def onAVStarted(self):
        logger.debug("--> onAVStarted")
        self._tracker.start()

    def onAVChange(self):
        logger.debug("--> onAVChange")

    def onPlayBackStarted(self):
        logger.debug("--> onPlayBackStarted")

    def onPlayBackEnded(self):
        logger.debug("--> onPlayBackEnded")

    def onPlayBackStopped(self):
        logger.debug("--> onPlayBackStopped")
        self._tracker.stop()

    def onPlayBackPaused(self):
        logger.debug("--> onPlayBackPaused")

    def onPlayBackResumed(self):
        logger.debug("--> onPlayBackResumed")

    def onPlayBackSeek(self):
        logger.debug("--> onPlayBackSeek")

    def onPlayBackSeekChapter(self):
        logger.debug("--> onPlayBackSeekChapter")
