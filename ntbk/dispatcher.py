import os
import config
import argparse
from pathlib import Path
from datetime import date
from datetime import date, timedelta
from commands import initialize, logfile

class Dispatcher():

    def __init__(self):
        initialize.init_app()
        self.config = config.load_config()
        self.parser = argparse.ArgumentParser(prog='ntbk', description='a terminal notebook application')
        self.subparsers = self.parser.add_subparsers(dest='command')
        self.configure_log_args()
        self.configure_collection_args()
        

    def run(self):
        args = self.parser.parse_args()
        args.func(args)


    def open_file_in_editor(self, file):
        """Creates directories, but not file. Its up to the user to save the file if they want it."""
        base_path = Path(self.config['ntbk_dir']).expanduser()
        file_path = Path(file)
        full_path = base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        os.system(f"{self.config['editor']} {full_path}")


    def open_logfile(self, args):
        date = args.date if args.command == 'date' else args.command
        file = logfile.get_logfile(date, args.file)
        self.open_file_in_editor(file)
        
    
    def configure_log_args(self):
        parser_today = self.subparsers.add_parser('today', help="Load today's log file")
        parser_today.add_argument('file', nargs='?', default=self.config['default_filename'])
        parser_today.set_defaults(func=self.open_logfile)

        parser_yest = self.subparsers.add_parser('yesterday', help="Load yesterday's log file")
        parser_yest.add_argument('file', nargs='?', default=self.config['default_filename'])
        parser_yest.set_defaults(func=self.open_logfile)

        parser_tom = self.subparsers.add_parser('tomorrow', help="Load tomorrow's log file")
        parser_tom.add_argument('file', nargs='?', default=self.config['default_filename'])
        parser_tom.set_defaults(func=self.open_logfile)

        parser_date = self.subparsers.add_parser('date', help="Load given date's log file")
        parser_date.add_argument('date', type=self.valid_date)
        parser_date.add_argument('file', nargs='?', default=self.config['default_filename'])
        parser_date.set_defaults(func=self.open_logfile)


    def configure_collection_args(self):
        pass


    def valid_date(self, s):
        try:
            return date.fromisoformat(s)
        except ValueError:
            msg = "not a valid date: {0!r}".format(s)
            raise argparse.ArgumentTypeError(msg)

