from pathlib import Path
import yaml

APP_CONFIG = {
    'config_filepath': '/home/blake/.config/ntbk/ntbk.yml'
}

_config_path = Path(APP_CONFIG['config_filepath']).expanduser()

def config_exists():
    return _config_path.exists()

def load_config():
    with _config_path.open() as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def save_config(config):
    _config_path.parent.mkdir(parents=True, exist_ok=True)
    _config_path.write_text(yaml.dump(config))
