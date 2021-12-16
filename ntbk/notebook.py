from pathlib import Path
from config import load_config

def notebook_exists():
    conf = load_config()
    return Path(conf['ntbk_dir']).expanduser().exists()

def create_notebook():
    conf = load_config()
    notebook_path = Path(conf['ntbk_dir']).expanduser()
    subfolders = ['_templates', 'collections', 'log']
    notebook_path.mkdir(parents=True, exist_ok=True)

    for sub in subfolders:
        (notebook_path / sub).mkdir(exist_ok=True)
    
    print(f'Created notebook at {notebook_path}')