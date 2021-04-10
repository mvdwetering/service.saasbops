import inspect
import logging
import os
import sys
from typing import List

import xbmcaddon

from resources.lib import common

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))

def execute(commands:List[str]) ->  None:
    command_handlers = [obj for name,obj in inspect.getmembers(sys.modules[__name__])
                        if (inspect.isfunction(obj) and
                            name.startswith('command_') and name in commands)]
    any(ch() for ch in command_handlers)


def command_reset_preferences() -> None:
    try:
        os.remove(common.get_preferences_filename())
    except FileNotFoundError:
        # Valid if no preferences were stored yet
        pass
    except Exception:
        logger.exception("Deleting preference file failed")
