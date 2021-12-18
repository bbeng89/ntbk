# system imports
import os
from pathlib import Path


class Filesystem():

    def __init__(self, config):
        self.config = config

    def get_notebook_base_path(self):
        return Path(self.config.get('ntbk_dir')).expanduser()

    def get_collection_base_path(self):
        return self.get_notebook_base_path() / 'collections'

    def get_log_base_path(self):
        return self.get_notebook_base_path() / 'log'

    def get_templates_base_path(self):
        return self.get_notebook_base_path() / self.config.get('template_dir')

    def create_file(self, filepath, content=None):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        if content is not None:
            filepath.write_text(content)
        else:
            filepath.touch()

    def append_to_file(self, filepath, content):
        with filepath.open(mode='a') as f:
            f.write(content)
    
    def open_file_in_editor(self, path):
        # TODO - need to escape the filename if it has spaces in it
        os.system(f"{self.config.get('editor')} {path}")

    