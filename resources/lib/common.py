import logging
import os

import xbmcaddon
import xbmcvfs

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo("id")

logger = logging.getLogger(ADDON_ID)

def get_storage_path() -> str:
    return os.path.join(xbmcvfs.translatePath("special://profile"), "addon_data", ADDON_ID)

def get_preferences_filename() -> str:
    return os.path.join(get_storage_path(), "data.json")
