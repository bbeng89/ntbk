import os
import argparse
from pathlib import Path
from actions import initialize, logfile
import config

def open_file_in_editor(file):
    """Creates directories, but not file. Its up to the user to save the file if they want it."""

    conf = config.load_config()
    base_path = Path(conf['ntbk_dir']).expanduser()
    file_path = Path(file)
    full_path = base_path / file_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    os.system(f"{conf['editor']} {full_path}")


if __name__ == '__main__':
    initialize.init_app()

    parser = argparse.ArgumentParser(prog='ntbk', description='a terminal notebook application')
    parser.add_argument('command')

    # todo - these will be used later for commands that have other args
    #subparsers = parser.add_subparsers()
    #parser_today = subparsers.add_parser('today', help="Load today's log file")
    
    args = parser.parse_args()

    if logfile.is_logfile_command(args.command):
        open_file_in_editor(logfile.get_logfile(args.command))
    