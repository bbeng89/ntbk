# system imports
import os
import argparse
from pathlib import Path
from datetime import date 

# 3rd party imports
from colorama import Fore, Style

# app imports
import config
from templater import Templater
from commands import initialize, logfile, template, collection


class Dispatcher():

    def __init__(self):
        # handles config and notebook directory
        initialize.init_app()

        # setup base argparser
        self.config = config.load_config()
        self.parser = argparse.ArgumentParser(prog='ntbk', description='NTBK - a simple terminal notebook application')
        self.subparsers = self.parser.add_subparsers(dest='command')

        # setup subparsers
        self.configure_log_args()
        self.configure_collection_args()
        self.configure_other_args()

    def run(self):
        args = self.parser.parse_args()
        args.func(args)

    def handle_logfile_command(self, args):
        dt = logfile.get_date(args.date if args.command == 'date' else args.command)
        file = self.get_full_path(logfile.filepath_for_date(dt, args.file))

        # Logfiles get an extra template variable - log_date. This is the date of the log file (not necessarily TODAY)
        extra_vars = { 'log_date': dt }

        if args.list:
            logfile.list_files_for_day(file.parent)
        else:
            if args.template: # check for template arg first to override default
                self.new_file_from_template(file, args.template, args.vars, extra_vars)
            elif self.config.get('default_templates', {}).get('log', {}).get(file.stem, None): # if no template arg, then check defaults
                template_file = f"{self.config['default_templates']['log'][file.stem]}.md"
                self.new_file_from_template(file, template_file, args.vars, extra_vars)
                
            self.open_file_in_editor(file)

    def handle_collection_command(self, args):
        file = self.get_full_path(collection.filepath_for_collection(args.collection_name, args.file))

        if args.list:
            collection.list_files_in_collection(file.parent)
        else:
            if args.template: # check for template arg first to override default
                self.new_file_from_template(file, args.template, args.vars)
            elif self.config.get('default_templates', {}).get('collection', {}).get(args.collection_name, None): # if no template arg, then check defaults
                template_file = f"{self.config['default_templates']['collection'][args.collection_name]}.md"
                self.new_file_from_template(file, template_file, args.vars)
            
            self.open_file_in_editor(file)

    def new_file_from_template(self, file, template, var_args=[], extra_vars={}):
        if file.exists() and file.read_text().strip():
            # reading the text and stripping it rather than looking at byte size so spaces/NLs are ignored
            #print(f"{Fore.YELLOW}Ignoring template because file already exists and is not empty.{Style.RESET_ALL}")
            return False
        else:
            templater = Templater()
            extra_vars.update(templater.convert_key_value_vars_to_dict(var_args))
            templater.create_file_from_template(template, str(file), extra_vars)
            return True

    def open_file_in_editor(self, path):
        # TODO - need to escape the filename if it has spaces in it
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
        parser_today.add_argument('--template', '-t', help='If creating, this template file will be used, overriding the default template')
        parser_today.add_argument("--vars", metavar="KEY=VALUE", nargs='+', default=[], help='Extra template variables in the format key=value. If value contains spaces, enclose it in quotes, e.g. key="my value"')
        parser_today.add_argument('--list', '-l', action='store_true', help="List today's files")
        parser_today.set_defaults(func=self.handle_logfile_command)

        parser_yest = self.subparsers.add_parser('yesterday', help="Load yesterday's log file")
        parser_yest.add_argument('file', nargs='?', default=self.config['default_filename'])
        parser_yest.add_argument('--template', '-t', help='If creating, this template file will be used, overriding the default template')
        parser_yest.add_argument("--vars", metavar="KEY=VALUE", nargs='+', default=[], help='Extra template variables in the format key=value. If value contains spaces, enclose it in quotes, e.g. key="my value"')
        parser_yest.add_argument('--list', '-l', action='store_true', help="List yesterday's files")
        parser_yest.set_defaults(func=self.handle_logfile_command)

        parser_tom = self.subparsers.add_parser('tomorrow', help="Load tomorrow's log file")
        parser_tom.add_argument('file', nargs='?', default=self.config['default_filename'])
        parser_tom.add_argument('--template', '-t', help='If creating, this template file will be used, overriding the default template')
        parser_tom.add_argument("--vars", metavar="KEY=VALUE", nargs='+', default=[], help='Extra template variables in the format key=value. If value contains spaces, enclose it in quotes, e.g. key="my value"')
        parser_tom.add_argument('--list', '-l', action='store_true', help="List tomorrow's files")
        parser_tom.set_defaults(func=self.handle_logfile_command)

        parser_date = self.subparsers.add_parser('date', help="Load given date's log file")
        parser_date.add_argument('date', type=self.valid_iso_date)
        parser_date.add_argument('file', nargs='?', default=self.config['default_filename'])
        parser_date.add_argument('--template', '-t', help='If creating, this template file will be used, overriding the default template')
        parser_date.add_argument("--vars", metavar="KEY=VALUE", nargs='+', default=[], help='Extra template variables in the format key=value. If value contains spaces, enclose it in quotes, e.g. key="my value"')
        parser_date.add_argument('--list', '-l', action='store_true', help="List given date's files")
        parser_date.set_defaults(func=self.handle_logfile_command)

    def configure_collection_args(self):
        parser_collection = self.subparsers.add_parser('collection', help="Load given collection")
        parser_collection.add_argument('collection_name')
        parser_collection.add_argument('file', nargs='?', default=self.config['default_filename'])
        parser_collection.add_argument('--template', '-t', help='If creating, this template file will be used, overriding the default template')
        parser_collection.add_argument("--vars", metavar="KEY=VALUE", nargs='+', default=[], help='Extra template variables in the format key=value. If value contains spaces, enclose it in quotes, e.g. key="my value"')
        parser_collection.add_argument('--list', '-l', action='store_true', help='List the files in given collection')
        parser_collection.set_defaults(func=self.handle_collection_command)

        parser_collections = self.subparsers.add_parser('collections', help="List all collections")
        parser_collections.set_defaults(func=collection.list_collections)

    def configure_other_args(self):
        parser_templates = self.subparsers.add_parser('templates', help="List all templates")
        parser_templates.set_defaults(func=template.list_templates)

    def valid_iso_date(self, s):
        """Validator used by argparse to make sure given dates are in ISO format"""
        try:
            return date.fromisoformat(s)
        except ValueError:
            msg = "not a valid date: {0!r}".format(s)
            raise argparse.ArgumentTypeError(msg)
