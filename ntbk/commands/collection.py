# system imports
from pathlib import Path

# 3rd party imports
from colorama import Fore, Style

# app imports
import config

def filepath_for_collection(collection, file):
    return f'collections/{collection}/{file}.md'

def get_files_in_collection(collection_path):
    files = []
    for child in collection_path.glob('*.*'):
        files.append(child)
    return files

def list_collections(args):
    conf = config.load_config()
    collection_dir = Path(conf['ntbk_dir']).expanduser() / 'collections'

    for child in collection_dir.glob('*/'):
        files = get_files_in_collection(child)
        countstr = f'{len(files)} {"file" if len(files) == 1 else "files"}'
        color = Fore.BLUE if len(files) == 1 else Fore.GREEN
        print(f'{child.relative_to(collection_dir)} {color}[{countstr}]{Style.RESET_ALL}')

