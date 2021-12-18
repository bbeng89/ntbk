# system imports
from pathlib import Path

# 3rd party imports
from colorama import Fore, Style

# app imports
import config


class CollectionCommand():

    def __init__(self, config, filesystem, collection_name, file_name):
        self.config = config
        self.filesystem = filesystem
        self.collection_name = collection_name
        self.file_name = file_name

    def get_relative_filepath(self):
        return f'collections/{self.collection_name}/{self.file_name}.md'

    def get_filepath(self):
        return self.filesystem.get_full_path(self.get_relative_filepath())

    def get_files_in_collection(self):
        files = []
        for child in self.get_filepath().parent.glob('*.*'):
            files.append(child)
        return files

    def list_files_in_collection(collection_path):
        for f in get_files_in_collection(collection_path):
            print(f.relative_to(collection_path))


class CollectionListCommand():

    def list_all_collections(self, config):
        collection_dir = Path(conf['ntbk_dir']).expanduser() / 'collections'

        for child in collection_dir.glob('*/'):
            files = get_files_in_collection(child)
            countstr = f'{len(files)} {"file" if len(files) == 1 else "files"}'
            color = Fore.BLUE if len(files) == 1 else Fore.GREEN
            print(f'{child.relative_to(collection_dir)} {color}[{countstr}]{Style.RESET_ALL}')