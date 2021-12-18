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

    def get_full_file_path(self, file_relative_path):
        """Gets the full path to the given file, creating all parent directories"""
        full_path = self.get_notebook_base_path() / file_relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        return full_path

    def create_file(self, out_file, content=None):
        out_path = Path(out_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if content is not None:
            out_path.write_text(content)

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

    