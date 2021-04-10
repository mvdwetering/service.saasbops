import sys

from resources.lib import kodilogging
from resources.lib import script_commands


kodilogging.config()

if __name__ == '__main__':
    script_commands.execute(sys.argv[1:])
