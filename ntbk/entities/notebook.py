# system imports
from pathlib import Path


class Notebook():

    def __init__(self, config):
        self.config = config
        self.notebook_path = Path(self.config.get('ntbk_dir')).expanduser()

    def exists(self):
        return self.notebook_path.exists()

    def create(self):
        template_dir = self.config.get('template_dir')
        subfolders = [template_dir, 'collections', 'log']

        self.notebook_path.mkdir(parents=True, exist_ok=True)

        for sub in subfolders:
            (self.notebook_path / sub).mkdir(exist_ok=True)
        
        # create a basic template for new log entries
        default_log_template = self.notebook_path / template_dir / 'log_default.md'
        default_log_template.write_text('# {{ today_long }}')
        
        print(f'Created notebook at {self.notebook_path}')
