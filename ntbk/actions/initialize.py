import os
import config
import notebook

def init_config_file():
    if not config.config_exists():
        config.save_config({
            'ntbk_dir': '',
            'editor': ''
            })

def init_notebook():
    if not config.config_exists():
        raise Exception("Can't initialize notebook until config file has been created")
    
    conf = config.load_config()

    if not conf['ntbk_dir']:
        conf['ntbk_dir'] = input('Enter notebook save directory (default = ~/ntbk): ') or '~/ntbk'
        config.save_config(conf)

    if not conf['editor']:
        conf['editor'] = input('Editor (will fallback to $EDITOR, then finally vim, if not specified):') or os.environ['EDITOR'] if 'EDITOR' in os.environ else 'vim'
        config.save_config(conf)
    
    if not notebook.notebook_exists():
        notebook.create_notebook()

def init_app():
    init_config_file()
    init_notebook()