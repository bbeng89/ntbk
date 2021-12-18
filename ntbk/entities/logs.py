# system imports
from datetime import date

# app imports
from templates import Template


class LogDate():
    def __init__(self, config, dt)
        self.config = config
        self.dt = dt

    def get_path():
        self.filesystem.get_logs_base_path() / f"{dt.strftime('%Y/%m-%B/%Y-%m-%d').lower()}" 

    def get_files():
        return [LogFile(self.config, self.filesystem, self.dt, child.stem) for child in self.get_path().glob('*.md')]


class LogFile():

    EXTENSION = '.md'

    def __init__(self, config, filesystem, dt, filename):
        self.config = config
        self.filesystem = filesystem
        self.logdate = LogDate(config, dt)
        self.filename = filename

    def get_path(self):
        return self.logdate.get_path() / f'{self.filename}{self.EXTENSION}'

    def get_name(self):
        return self.filename

    def get_default_template_name(self):
        return self.config\
            .get('default_templates', {})\
            .get('log', {})\
            .get(self.filename, None)

    def has_default_template(self):
        return self.get_default_template_name() is not None

    def get_default_template(self):
        if not self.has_default_template():
            return None
        return Template(self.config, self.filesystem, self.get_default_template_name())
