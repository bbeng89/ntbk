# system imports
from datetime import date

# app imports
from ntbk.entities.templates import Template


class LogDate():
    """This class represents a day in the log/ directory. It has 1-n LogFiles"""

    def __init__(self, config, filesystem, dt):
        self.config = config
        self.filesystem = filesystem
        self.dt = dt

    def get_path(self):
        """Get the pathlib.Path object to this log date (will be a folder)"""
        return self.filesystem.get_log_base_path() / f"{self.dt.strftime('%Y/%m-%B/%Y-%m-%d').lower()}" 

    def get_files(self):
        """Get all the files for this log date"""
        return [LogFile(self.config, self.filesystem, self.dt, child.stem) for child in self.get_path().glob('*.md')]


class LogFile():
    """This class represents a file inside a LogDate"""

    EXTENSION = '.md'

    def __init__(self, config, filesystem, dt, filename):
        self.config = config
        self.filesystem = filesystem
        self.logdate = LogDate(config, filesystem, dt)
        self.filename = filename

    def get_path(self):
        """Get the pathlib.Path object to this log date file"""
        return self.logdate.get_path() / f'{self.filename}{self.EXTENSION}'

    def get_name(self):
        """Get the name of this file (without extension)"""
        return self.filename

    def exists(self):
        """Whether or not this file exists on disk"""
        return self.get_path().exists()

    def is_empty(self):
        """Whether or not this file exists and has any content in it (spaces and newlines dont count)"""
        if not self.get_path().exists():
            return True
        return bool(self.get_path().read_text().strip())

    def get_default_template_name(self):
        """Get the default template name for this file as defined in the config file. Returns None if there isn't one."""
        return self.config\
            .get('default_templates', {})\
            .get('log', {})\
            .get(self.filename, None)

    def has_default_template(self):
        """Whether or not this file has a default template defined in the config file"""
        return self.get_default_template_name() is not None

    def get_default_template(self):
        """Get the default template Template object for this file. Returns None if there isn't one."""
        if not self.has_default_template():
            return None
        return Template(self.config, self.filesystem, self.get_default_template_name())
