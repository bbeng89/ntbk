# system imports
import sys

# 3rd party imports
import colorama

# app imports
import initialize
from config import Config
from dispatcher import Dispatcher
from templater import Templater
from filesystem import Filesystem
from exceptions import InvalidConfigException


if __name__ == '__main__':
    try:
        config = Config()
        filesystem = Filesystem(config)

        colorama.init()
        initialize.init_app(config)
        Dispatcher(config, filesystem).run()
    except InvalidConfigException as e:
        print(e, file=sys.stderr)
        sys.exit(1)