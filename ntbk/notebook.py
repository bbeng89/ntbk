# system imports
from pathlib import Path

# app imports
from config import load_config


def notebook_exists():
    conf = load_config()
    return Path(conf['ntbk_dir']).expanduser().exists()


def create_notebook():
    conf = load_config()
    notebook_path = Path(conf['ntbk_dir']).expanduser()
    subfolders = [conf['template_dir'], 'collections', 'log']
    notebook_path.mkdir(parents=True, exist_ok=True)

    for sub in subfolders:
        (notebook_path / sub).mkdir(exist_ok=True)
    
    # create a basic template for new log entries
    default_log_template = notebook_path / conf['template_dir'] / 'log_default.md'
    default_log_template.write_text('# {{ today_long }}')
    
    print(f'Created notebook at {notebook_path}')