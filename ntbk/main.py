import argparse
from actions.initialize import initialize
import config
import notebook

def init_config_file():
    if not config.config_exists():
        config.save_config({'ntbk_dir': ''})

def init_notebook():
    if not config.config_exists():
        raise Exception("Can't initialize notebook until config file has been created")
    
    conf = config.load_config()

    if not conf['ntbk_dir']:
        conf['ntbk_dir'] = input('Enter notebook save directory (default = ~/ntbk): ') or '~/ntbk'
        config.save_config(conf)
    
    if not notebook.notebook_exists():
        notebook.create_notebook()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ntbk - a terminal notebook application')
    parser.add_argument('command')
    args = parser.parse_args()

    init_config_file()
    init_notebook()