import logging
from typing import Any, Dict, Optional

import xbmcaddon

ADDON = xbmcaddon.Addon()
addon_id = ADDON.getAddonInfo('id')
logger = logging.getLogger(addon_id)


class Preferences():
    def __init__(self, load, save) -> None:
        self._storage = {}
        self._load = load
        self._save = save

        if self._load:
            self._storage = self._load()

    def reset(self, ) -> None:
        self._storage = {}

    def get(self, show: int, season: int, episode: int) -> Optional[Dict]:
        # Strings to allow for storing as JSON (easier debugging than binary formats)
        show_str = str(show)

        if show_str not in self._storage.keys():
            return None
        for s in reversed(range(0, season+1)):
            for e in reversed(range(0, episode+1)):
                try:
                    info = self._storage[show_str][str(s)][str(e)]
                    return info
                except KeyError:
                    pass

    def set(self, show: int, season: int, episode: int, info: Any) -> None:
        # Strings to allow for storing as JSON (easier debugging than binary formats)
        show = str(show)
        season = str(season)
        episode = str(episode)

        if show not in self._storage.keys():
            self._storage[show] = {}
        if season not in self._storage[show].keys():
            self._storage[show][season] = {}

        self._storage[show][season][episode] = info
        logger.debug("Stored show: %s, season:%s, episode:%s, info:%s",
                     show, season, episode, str(info))
        if self._save:
            self._save(self._storage)
