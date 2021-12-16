# 3rd party imports
import colorama

# app imports
from dispatcher import Dispatcher

dispatcher = Dispatcher()

if __name__ == '__main__':
    colorama.init()
    dispatcher.run()
    