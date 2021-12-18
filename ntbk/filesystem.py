# system imports
import os
from pathlib import Path


class Filesystem():
    """This class should be the basis for all interactions with the filesystem including retrieving paths and creating files"""

    def __init__(self, config):
        self.config = config

    def get_notebook_base_path(self):
        """Get the pathlib.Path object to the notebook root folder"""
        return Path(self.config.get('ntbk_dir')).expanduser()

    def get_collection_base_path(self):
        """Get the pathlib.Path object to the collections folder"""
        return self.get_notebook_base_path() / 'collections'

    def get_log_base_path(self):
        """Get the pathlib.Path object to the log folder"""
        return self.get_notebook_base_path() / 'log'

    def get_templates_base_path(self):
        """Get the pathlib.Path object to the _templates folder (or whatever is configured)"""
        return self.get_notebook_base_path() / self.config.get('template_dir')

    def create_file(self, filepath, content=None):
        """Create a file (filepath must be a Path object) optionally with the given content. Parent directories will be created."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        if content is not None:
            filepath.write_text(content)
        else:
            filepath.touch()

    def append_to_file(self, filepath, content):
        """Write content to the end of the given file (filepath must be a Path object)"""
        with filepath.open(mode='a') as f:
            f.write(content)
    
    def open_file_in_editor(self, path):
        """Open the given path in the configured editor. Can be a string or Path object, but must be the absolute path"""
        # TODO - need to escape the filename if it has spaces in it
        os.system(f"{self.config.get('editor')} {path}")
