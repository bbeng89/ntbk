# system imports
from datetime import date, timedelta

class LogFileCommand():

    def __init__(self, config, filesystem, command, filename, specific_date = None):
        self.config = config
        self.filesystem = filesystem
        self.command = command
        self.filename = filename
        self.specific_date = specific_date

    def is_empty_command(self):
        return self.command is None

    def is_specific_date_command(self):
        return self.command == 'date' and isinstance(self.specific_date, date)

    def has_default_template(self):
        return self.get_default_template is not None

    def get_default_template_name(self):
        return self.config\
            .get('default_templates', {})\
            .get('log', {})\
            .get(self.get_filepath().stem, None)

    def get_filepath(self):
        return self.filesystem.get_full_path(self.get_relative_filepath())

    def get_relative_filepath(self):
        dt = self.get_date_object()

        if dt is None:
            return None

        return f"log/{dt.strftime('%Y/%m-%B/%Y-%m-%d').lower()}/{self.filename}.md"

    def get_extra_vars(self):
        return { 'log_date': self.get_date_object() }

    def get_date_object(self):
        if self.is_specific_date_command():
            return self.specific_date
        elif self.command == 'today':
            return date.today()
        elif self.command == 'yesterday':
            return date.today() - timedelta(days=1)
        elif self.command == 'tomorrow':
            return date.today() + timedelta(days=1)

        return None

    def get_files_for_day(self):
        files = []
        for child in self.get_filepath().parent.glob('*.*'):
            files.append(child)
        return files

    def list_files_for_day(self):
        for f in self.get_files_for_day():
            print(f.relative_to(self.get_filepath().parent))