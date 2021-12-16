from pathlib import Path
import yaml

APP_CONFIG = {
    'config_filepath': '~/.config/ntbk/ntbk.yml'
}
CONFIG_DEFAULTS = {
    'ntbk_dir': '',
    'editor': '',
    'default_filename': 'index',
    'template_dir': '_templates'
    }

_config_path = Path(APP_CONFIG['config_filepath']).expanduser()

def config_exists():
    return _config_path.exists()

def load_config():
    with _config_path.open() as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def validate_config():
    config = load_config()
    for key, val in CONFIG_DEFAULTS.items():
        if key not in config or not config[key]:
            raise Exception('Configuration file is not valid')

def save_config(config):
    _config_path.parent.mkdir(parents=True, exist_ok=True)
    _config_path.write_text(yaml.dump(config))

