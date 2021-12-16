import os
import config
import argparse
from pathlib import Path
from datetime import date 
from commands import initialize, logfile
from templater import Templater

class Dispatcher():

    def __init__(self):
        initialize.init_app()
        self.config = config.load_config()
        self.parser = argparse.ArgumentParser(prog='ntbk', description='NTBK - a simple terminal notebook application')
        self.parser.add_argument('--template', '-t', help='If creating, this template file will be used, overriding the default template')
        self.subparsers = self.parser.add_subparsers(dest='command')
        self.configure_log_args()
        self.configure_collection_args()
        

    def run(self):
        args = self.parser.parse_args()
        args.func(args)


    def handle_logfile_command(self, args):
        d = args.date if args.command == 'date' else args.command
        file = self.get_full_path(logfile.get_logfile(d, args.file))

        if args.template: # check for template arg first to override default
            self.handle_template(file, args.template)
        elif 'default_log_template' in self.config and self.config['default_log_template']: # if no template arg, then check defaults
            self.handle_template(file, self.config['default_log_template'])
            
        self.open_file_in_editor(file)


    def handle_template(self, file, template):
        if file.exists() and file.read_text().strip():
            # reading the text and stripping it rather than looking at byte size so spaces/NLs are ignored
            print("Ignoring template because file already exists and is not empty.")
            return False
        else:
            templater = Templater()
            templater.create_file_from_template(template, str(file))
            return True


    def open_file_in_editor(self, path):
        os.system(f"{self.config['editor']} {path}")


    def get_full_path(self, file):
        """Gets the full path to the given file, creating all parent directories"""

        base_path = Path(self.config['ntbk_dir']).expanduser()
        file_path = Path(file)
        full_path = base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        return full_path

            
    def configure_log_args(self):
        parser_today = self.subparsers.add_parser('today', help="Load today's log file")
        parser_today.add_argument('file', nargs='?', default=self.config['default_filename'])
        parser_today.set_defaults(func=self.handle_logfile_command)

        parser_yest = self.subparsers.add_parser('yesterday', help="Load yesterday's log file")
        parser_yest.add_argument('file', nargs='?', default=self.config['default_filename'])
        parser_yest.set_defaults(func=self.handle_logfile_command)

        parser_tom = self.subparsers.add_parser('tomorrow', help="Load tomorrow's log file")
        parser_tom.add_argument('file', nargs='?', default=self.config['default_filename'])
        parser_tom.set_defaults(func=self.handle_logfile_command)

        parser_date = self.subparsers.add_parser('date', help="Load given date's log file")
        parser_date.add_argument('date', type=self.valid_iso_date)
        parser_date.add_argument('file', nargs='?', default=self.config['default_filename'])
        parser_date.set_defaults(func=self.handle_logfile_command)


    def configure_collection_args(self):
        pass


    def valid_iso_date(self, s):
        """Validator used by argparse to make sure given dates are in ISO format"""
        try:
            return date.fromisoformat(s)
        except ValueError:
            msg = "not a valid date: {0!r}".format(s)
            raise argparse.ArgumentTypeError(msg)

