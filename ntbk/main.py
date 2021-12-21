"""Main entry point into the application"""

# system imports
import sys

# 3rd party imports
import colorama

# app imports
from ntbk import initialize
from ntbk.config import Config
from ntbk.dispatcher import Dispatcher
from ntbk.filesystem import Filesystem
from ntbk.exceptions import InvalidConfigException

def run():
    """Run the application"""
    try:
        config = Config()
        filesystem = Filesystem(config)
        colorama.init()
        initialize.init_app(config)
        Dispatcher(config, filesystem).run(sys.argv[1:])
    except InvalidConfigException as err:
        print(err, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    run()
