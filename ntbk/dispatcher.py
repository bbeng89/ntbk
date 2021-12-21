# system imports
import argparse
from datetime import datetime, date 

# 3rd party imports
from colorama import Fore, Style

# app imports
from ntbk import helpers
from ntbk.entities.collections import CollectionFile, get_all_collections
from ntbk.entities.logs import LogFile
from ntbk.entities.templates import Template, get_all_templates


class Dispatcher():
    """This class is responsible for parsing arguments to the program and handling them appropriately"""

    def __init__(self, config, filesystem):
        self.config = config
        self.filesystem = filesystem
        self.parser = argparse.ArgumentParser(prog='ntbk', description='NTBK - a simple terminal notebook application')
        # set all these defaults so that it will run without any args. This will default to the "today" command
        self.parser.set_defaults(func=self.handle_logfile_command, file=self.config.get('default_filename'), list=False, find=False, find_dir=False, template=None, vars=[])
        self.subparsers = self.parser.add_subparsers(dest='command')

        # setup subparsers
        self.configure_log_args()
        self.configure_collection_args()
        self.configure_other_args()

    def run(self, sys_args):
        """Parse the args passed into the program and call the appropriate handler function"""
        args = self.parser.parse_args(sys_args)
        args.func(args)

    def open_or_create_entity(self, args, entity):
        """Open or create either a log or collection file. Entity must be either LogFile or CollectionFile"""
        template = None

        entity.create_directories()

        if not entity.exists():
            if args.template: 
                template = Template(self.config, self.filesystem, args.template)
            elif entity.has_default_template(): 
                template = entity.get_default_template()
                
            if template is not None:
                vars = {}
                if isinstance(entity, LogFile):
                    vars['log_date'] = entity.get_logdate().get_date()
                vars.update(helpers.convert_key_value_vars_to_dict(args.vars))
                template.set_extra_vars(vars)
                self.filesystem.create_file(entity.get_path(), template.render())

        self.filesystem.open_file_in_editor(entity.get_path())

    def list_entities(self, entities):
        """Takes a list of LogFile or CollectionFile objects and prints out their names"""
        for e in entities:
            print(e.get_name())

    def handle_logfile_command(self, args):
        """Handler for commands involving log files"""
        if args.command is None:
            args.command = 'today'

        dt = args.date if args.command == 'date' else helpers.get_date_object_for_alias(args.command)
        logfile = LogFile(self.config, self.filesystem, dt, args.file)
        if args.list:
            self.list_entities(logfile.logdate.get_files())
        elif args.find:
            print(logfile.get_path())
        elif args.find_dir:
            print(logfile.get_logdate().get_path())
        else:
            self.open_or_create_entity(args, logfile)
            
    def handle_collection_command(self, args):
        """Handler for commands involving collection files"""
        collection_file = CollectionFile(self.config, self.filesystem, args.collection_name, args.file)
        if args.list:
            self.list_entities(collection_file.collection.get_files())
        elif args.find:
            print(collection_file.get_path())
        elif args.find_dir:
            print(collection_file.get_collection().get_path())
        else:
            self.open_or_create_entity(args, collection_file)

    def handle_list_collections_command(self, args):
        """Handler for the 'collections' command - lists all the collections"""
        for c in get_all_collections(self.config, self.filesystem):
            fcount = c.get_file_count()
            countstr = f'{fcount} {"file" if fcount == 1 else "files"}'
            color = Fore.BLUE if fcount == 1 else Fore.GREEN
            print(f'{c.get_name()} {color}[{countstr}]{Style.RESET_ALL}')

    def handle_list_templates_command(self, args):
        """Handler for the 'templates' command - lists all the available templates"""
        for template in get_all_templates(self.config, self.filesystem):
            print(template.get_name())

    def handle_jot_command(self, args):
        """Handler for the 'jot' command. Appends the given text to today's file, optionally with a timestamp"""
        dt = helpers.get_date_object_for_alias('today')
        logfile = LogFile(self.config, self.filesystem, dt, args.file)
        content = args.text
        if args.timestamp:
            content = f"[{datetime.now().strftime('%I:%M %p')}]\n" + content
        content = '\n\n' + content

        self.filesystem.append_to_file(logfile.get_path(), content)
        print(f"{Fore.GREEN}Jotted note to today's {logfile.get_name()} file{Style.RESET_ALL}")
        
    def configure_log_args(self):
        """Configure all the possible args for commands involving log files"""
        default_file = self.config.get('default_filename')
        parser_today = self.subparsers.add_parser('today', help="Load today's log file")
        parser_today.add_argument('file', nargs='?', default=default_file)
        parser_today.add_argument('--template', '-t', help='If creating, this template file will be used, overriding the default template')
        parser_today.add_argument("--vars", metavar="KEY=VALUE", nargs='+', default=[], help='Extra template variables in the format key=value. If value contains spaces, enclose it in quotes, e.g. key="my value"')
        parser_today.add_argument('--list', '-l', action='store_true', help="List today's files")
        parser_today.add_argument('--find', '-f', action='store_true', help="Output the path to the file")
        parser_today.add_argument('--find-dir', '-d', action='store_true', help="Output the path to the file's directory")
        parser_today.set_defaults(func=self.handle_logfile_command)

        parser_yest = self.subparsers.add_parser('yesterday', help="Load yesterday's log file")
        parser_yest.add_argument('file', nargs='?', default=default_file)
        parser_yest.add_argument('--template', '-t', help='If creating, this template file will be used, overriding the default template')
        parser_yest.add_argument("--vars", metavar="KEY=VALUE", nargs='+', default=[], help='Extra template variables in the format key=value. If value contains spaces, enclose it in quotes, e.g. key="my value"')
        parser_yest.add_argument('--list', '-l', action='store_true', help="List yesterday's files")
        parser_yest.add_argument('--find', '-f', action='store_true', help="Output the path to the file")
        parser_yest.add_argument('--find-dir', '-d', action='store_true', help="Output the path to the file's directory")
        parser_yest.set_defaults(func=self.handle_logfile_command)

        parser_tom = self.subparsers.add_parser('tomorrow', help="Load tomorrow's log file")
        parser_tom.add_argument('file', nargs='?', default=default_file)
        parser_tom.add_argument('--template', '-t', help='If creating, this template file will be used, overriding the default template')
        parser_tom.add_argument("--vars", metavar="KEY=VALUE", nargs='+', default=[], help='Extra template variables in the format key=value. If value contains spaces, enclose it in quotes, e.g. key="my value"')
        parser_tom.add_argument('--list', '-l', action='store_true', help="List tomorrow's files")
        parser_tom.add_argument('--find', '-f', action='store_true', help="Output the path to the file")
        parser_tom.add_argument('--find-dir', '-d', action='store_true', help="Output the path to the file's directory")
        parser_tom.set_defaults(func=self.handle_logfile_command)

        parser_date = self.subparsers.add_parser('date', help="Load given date's log file")
        parser_date.add_argument('date', type=helpers.argparse_valid_iso_date)
        parser_date.add_argument('file', nargs='?', default=default_file)
        parser_date.add_argument('--template', '-t', help='If creating, this template file will be used, overriding the default template')
        parser_date.add_argument("--vars", metavar="KEY=VALUE", nargs='+', default=[], help='Extra template variables in the format key=value. If value contains spaces, enclose it in quotes, e.g. key="my value"')
        parser_date.add_argument('--list', '-l', action='store_true', help="List given date's files")
        parser_date.add_argument('--find', '-f', action='store_true', help="Output the path to the file")
        parser_date.add_argument('--find-dir', '-d', action='store_true', help="Output the path to the file's directory")
        parser_date.set_defaults(func=self.handle_logfile_command)

    def configure_collection_args(self):
        """Configure all the possible args for commands involving collection files"""
        default_file = self.config.get('default_filename')
        parser_collection = self.subparsers.add_parser('collection', help="Load given collection")
        parser_collection.add_argument('collection_name')
        parser_collection.add_argument('file', nargs='?', default=default_file)
        parser_collection.add_argument('--template', '-t', help='If creating, this template file will be used, overriding the default template')
        parser_collection.add_argument("--vars", metavar="KEY=VALUE", nargs='+', default=[], help='Extra template variables in the format key=value. If value contains spaces, enclose it in quotes, e.g. key="my value"')
        parser_collection.add_argument('--list', '-l', action='store_true', help='List the files in given collection')
        parser_collection.add_argument('--find', '-f', action='store_true', help="Output the path to the file")
        parser_collection.add_argument('--find-dir', '-d', action='store_true', help="Output the path to the file's directory")
        parser_collection.set_defaults(func=self.handle_collection_command)

        parser_collections = self.subparsers.add_parser('collections', help="List all collections")
        parser_collections.set_defaults(func=self.handle_list_collections_command)

    def configure_other_args(self):
        """Configure args for any other commands"""
        default_file = self.config.get('default_filename')
        parser_templates = self.subparsers.add_parser('templates', help="List all templates")
        parser_templates.set_defaults(func=self.handle_list_templates_command)

        parser_jot = self.subparsers.add_parser('jot', help="Add a quick note to today's log without opening your editor")
        parser_jot.add_argument('text')
        parser_jot.add_argument('file', nargs='?', default=default_file, help="Jot to file other than the default")
        parser_jot.add_argument('--timestamp', '-s', action='store_true', help="Add a timestamp before the jotted note")
        parser_jot.set_defaults(func=self.handle_jot_command)
