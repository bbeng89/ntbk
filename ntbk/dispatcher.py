# system imports
import argparse
from datetime import date 

# app imports
import helpers
from entities.collections import Collection, CollectionFile, get_all_collections
from entities.logs import LogDate, LogFile
from entities.templates import Template, get_all_templates


class Dispatcher():

    def __init__(self, config, filesystem):

        self.config = config
        self.filesystem = filesystem
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

    def open_or_create_entity(self, entity):
        template = None

        if args.template: 
            template = Template(self.config, self.filesystem, args.template)
        elif entity.has_default_template(): 
            template = entity.get_default_template()
            
        if template is not None:
            template.set_extra_vars(helpers.convert_key_value_vars_to_dict(args.vars))
            filesystem.create_file(entity.get_path(), template.render())

        self.filesystem.open_file_in_editor(entity.get_path())

    def list_entities(self, entities):
        for e in entities:
            print(e.get_name())

    def handle_logfile_command(self, args):
        dt = args.date if args.command == 'date' else helpers.get_date_object_for_alias(args.command)
        logfile = LogFile(self.config, self.filesystem, dt, args.file)
        if args.list:
            self.list_entities(logfile.logdate.get_files())
        else:
            self.open_or_create_entity(logfile)
            
    def handle_collection_command(self, args):
        collection_file = CollectionFile(self.config, self.filesystem, args.collection_name, args.file)
        if args.list:
            self.list_entities(collection_file.collection.get_files())
        else:
            self.open_or_create_entity(collection_file)

    def handle_list_collections_command(self, args):
        for c in get_all_collections(self.config, self.filesystem):
            fcount = c.get_file_count()
            countstr = f'{fcount} {"file" if fcount == 1 else "files"}'
            color = Fore.BLUE if fcount == 1 else Fore.GREEN
            print(f'{c.get_name()} {color}[{countstr}]{Style.RESET_ALL}')

    def handle_list_templates_command(self, args):
        for template in get_all_templates(self.config, self.filesystem):
            print(template.get_name())

    def handle_jot_command(self, args):
        dt = helpers.get_date_object_for_alias('today')
        logfile = LogFile(self.config, self.filesystem, dt, args.file)
        content = args.text
        if args.timestamp:
            content = f"[{datetime.now().strftime('%I:%M %p')}]\n" + content

        filesystem.append_to_file(logfile.get_path(), content)
        
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
