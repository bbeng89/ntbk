# system imports
from pathlib import Path

# 3rd party imports
import yaml


class Config():

    CONFIG_FILEPATH = '~/.config/ntbk/ntbk.yml'

    DEFAULTS = {
        'ntbk_dir': '',
        'editor': '',
        'default_filename': 'index',
        'template_dir': '_templates',
        'default_templates': {
            'log': {
                'index': 'log_default'
            }
        },
        'template_vars': {
            'foo': 'bar'
        }
    }

    REQUIRED_KEYS = ['ntbk_dir', 'editor', 'template_dir']
    
    _config = {}

    def __init__(self):
        self._config_path = Path(self.CONFIG_FILEPATH).expanduser()
        self.load()

    def get(self, key, default=None):
        return self._config.get(key, default)

    def set(self, key, value):
        self._config[key] = value
        self.save()

    def save(self):
        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        self._config_path.write_text(yaml.dump(self._config))

    def is_valid(self):
        for key in self.REQUIRED_KEYS:
            if key not in self._config or not self._config[key]:
                return False
        return True

    def load(self):
        if self.config_file_exists():
            with self._config_path.open() as file:
                self._config = yaml.load(file, Loader=yaml.FullLoader)

    def config_file_exists(self):
        return self._config_path.exists()

    def reset_to_defaults(self):
        self._config = self.DEFAULTS
        self.save()

