# system imports
from pathlib import Path

# app imports
import config

def filepath_for_collection(collection, file):
    return f'collections/{collection}/{file}.md'

def list_collections(args):
    conf = config.load_config()
    collection_dir = Path(conf['ntbk_dir']).expanduser() / 'collections'
    for child in collection_dir.glob('*/'):
        filecount = 0
        for f in child.glob('*.*'):
            filecount += 1
        countstr = f'{filecount} {"file" if filecount == 1 else "files"}'
        print(f'{child.relative_to(collection_dir)} [{countstr}]')

