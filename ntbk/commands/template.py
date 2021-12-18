# system imports
from pathlib import Path

# 3rd party imports
from colorama import Fore, Style

# app imports
import config

def is_default_template(type, template):
    conf = config.load_config()
    log_defaults = conf.get('default_templates', {}).get(type, None)
    if log_defaults is not None:
        for f, t in log_defaults.items():
            if t == template:
                return { 'is_default': True, 'for': f}
    
    return { 'is_default': False }



def list_templates():
    conf = config.load_config()
    template_dir = Path(conf['ntbk_dir']).expanduser() / conf['template_dir']
    
    if not template_dir.exists():
        print('Template directory does not exist. Please check your config file.')
    if not template_dir.is_dir():
        print('Provided template path is not a directory')
    else:
        for child in template_dir.glob('**/*.*'):
            name = str(child.relative_to(template_dir))
            log_default = is_default_template('log', str(child.relative_to(template_dir).stem))
            col_default = is_default_template('collection', str(child.relative_to(template_dir).stem))
            if log_default['is_default']:
                name += f"{Fore.GREEN} [log default: '{log_default['for']}' files] {Style.RESET_ALL}"
            elif col_default['is_default']:
                name += f"{Fore.CYAN} [collection default: '{col_default['for']}' files] {Style.RESET_ALL}"

            print(name)
