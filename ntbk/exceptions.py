
class InvalidConfigException(Exception):

    def __init__(self):
        super().__init__('Configuration file is not valid. Please review the docs and check your config file.')