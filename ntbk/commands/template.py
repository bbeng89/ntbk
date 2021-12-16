# system imports
from pathlib import Path

# 3rd party imports
from colorama import Fore, Style

# app imports
import config


def list_templates(args):
    conf = config.load_config()
    template_dir = Path(conf['ntbk_dir']).expanduser() / conf['template_dir']
    
    if not template_dir.exists():
        print('Template directory does not exist. Please check your config file.')
    if not template_dir.is_dir():
        print('Provided template path is not a directory')
    else:
        for child in template_dir.glob('**/*.*'):
            name = str(child.relative_to(template_dir.parent))
            if str(child.relative_to(template_dir)) == conf['default_log_template']:
                name += f'{Fore.GREEN} [log default] {Style.RESET_ALL}'
            elif str(child.relative_to(template_dir)) == conf['default_collection_template']:
                name += f'{Fore.GREEN} [collection default] {Style.RESET_ALL}'

            print(name)
