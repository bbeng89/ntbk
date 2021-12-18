# system imports
import argparse
from datetime import date 

# app imports
from commands.logfile import LogFileCommand
from commands import logfile, template, collection, jot


class Dispatcher():

    def __init__(self, config, filesystem):

        self.config = config
        self.filesystem = filesystem

        # setup base argparser
        self.parser = argparse.ArgumentParser(prog='ntbk', description='NTBK - a simple terminal notebook application')
        # set all these defaults so that it will run without any args. This will default to the "today" command
        self.parser.set_defaults(func=self.handle_logfile_command, file=self.config.get('default_filename'), list=False, template=None, vars=[])
        self.subparsers = self.parser.add_subparsers(dest='command')

        # setup subparsers
        self.configure_log_args()
        self.configure_collection_args()
        self.configure_other_args()

    def run(self):
        args = self.parser.parse_args()
        args.func(args)

    def handle_logfile_command(self, args):
        log_command = LogFileCommand(self.config, self.filesystem, args.command, args.file, args.date if args.command == 'date' else None)

        if args.list:
            log_command.list_files_for_day()
        else:
            file = log_command.get_filepath()

            if args.template: 
                self.filesystem.new_file_from_template(file, args.template, args.vars, log_command.get_extra_vars())
            elif log_command.has_default_template(): 
                template_file = f"{log_command.get_default_template_name()}.md"
                self.filesystem.new_file_from_template(file, template_file, args.vars, log_command.get_extra_vars())
                
            self.filesystem.open_file_in_editor(file)

    def handle_collection_command(self, args):
        file = self.filesystem.get_full_path(collection.filepath_for_collection(args.collection_name, args.file))

        if args.list:
            collection.list_files_in_collection(file.parent)
        else:
            # check for template arg first to override default
            if args.template: 
                self.filesystem.new_file_from_template(file, args.template, args.vars)
            # if no template arg, then check defaults
            elif self.config.get('default_templates', {}).get('collection', {}).get(args.collection_name, None): 
                template_file = f"{self.config.get('default_templates').get('collection').get(args.collection_name)}.md"
                self.new_file_from_template(file, template_file, args.vars)
            
            self.open_file_in_editor(file)

    def handle_list_collections_command(self, args):
        collection.list_collections()

    def handle_list_templates_command(self, args):
        template.list_templates()

    def handle_jot_command(self, args):
        dt = logfile.get_date('today')
        file = self.filesystem.get_full_path(logfile.filepath_for_date(dt, args.file))
        jot.jot_note(args.text, file, args.timestamp)

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
        parser_collections.set_defaults(func=self.handle_list_collections_command)

    def configure_other_args(self):
        parser_templates = self.subparsers.add_parser('templates', help="List all templates")
        parser_templates.set_defaults(func=self.handle_list_templates_command)

        parser_jot = self.subparsers.add_parser('jot', help="Add a quick note to today's log without opening your editor")
        parser_jot.add_argument('text')
        parser_jot.add_argument('file', nargs='?', default=self.config['default_filename'], help="Jot to file other than the default")
        parser_jot.add_argument('--timestamp', '-s', action='store_true', help="Add a timestamp before the jotted note")
        parser_jot.set_defaults(func=self.handle_jot_command)

    def valid_iso_date(self, s):
        """Helper: Validator used by argparse to make sure given dates are in ISO format"""
        try:
            return date.fromisoformat(s)
        except ValueError:
            msg = "not a valid date: {0!r}".format(s)
            raise argparse.ArgumentTypeError(msg)
