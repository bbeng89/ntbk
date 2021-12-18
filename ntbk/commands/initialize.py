# system imports
import os

# app imports
from notebook import Notebook
from exceptions import InvalidConfigException


def init_config_file(config):
    if not config.config_exists():
        config.reset_to_defaults()

    if not config.is_valid():
        raise InvalidConfigException()


def init_notebook(config):
    if not config.is_valid():
        raise InvalidConfigException()
    
    if not config.get('ntbk_dir'):
        ntbk_dir = input('Enter notebook save directory (default = ~/ntbk): ') or '~/ntbk'
        config.set('ntbk_dir', ntbk_dir)

    if not config.get('editor'):
        editor = input('Editor (will fallback to $EDITOR, then finally vim, if not specified):') or os.environ['EDITOR'] if 'EDITOR' in os.environ else 'vim'
        config.set('editor', editor)
    
    notebook = Notebook(config)
    
    if not notebook.notebook_exists():
        notebook.create_notebook()


def init_app(config):
    init_config_file(config)
    init_notebook(config)