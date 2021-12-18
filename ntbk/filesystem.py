# system imports
import os
from pathlib import Path


class Filesystem():

    def __init__(self, config, templater):
        self.config = config
        self.templater = templater

    def get_notebook_base_path(self):
        return Path(self.config.get('ntbk_dir')).expanduser()

    def get_collection_base_path(self):
        return self.get_notebook_base_path() / 'collections'

    def get_logs_base_path(self):
        return self.get_notebook_base_path() / 'logs'

    def get_templates_base_path(self):
        return self.get_notebook_base_path() / self.config.get('template_dir')

    def create_file(self, filepath, content=None):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        if content is not None:
            filepath.write_text(content)
        else:
            filepath.touch()

    def append_to_file(self, filepath, content):
        with file_path.open(mode='a') as f:
            f.write(content)

    def new_file_from_template(self, file, template, var_args=[], extra_vars={}):
        if file.exists() and file.read_text().strip():
            # reading the text and stripping it rather than looking at byte size so spaces/NLs are ignored
            return False

        extra_vars.update(self.templater.convert_key_value_vars_to_dict(var_args))
        self.templater.create_file_from_template(template, str(file), extra_vars)
        return True

    def open_file_in_editor(self, path):
        # TODO - need to escape the filename if it has spaces in it
        os.system(f"{self.config.get('editor')} {path}")

    