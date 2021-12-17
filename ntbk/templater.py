# system imports
from pathlib import Path
from datetime import date, datetime

# 3rd party imports
from jinja2 import Environment, FileSystemLoader

# app imports
import config


class Templater():

    def __init__(self):
        self.config = config.load_config()
        self.template_path = Path(self.config['ntbk_dir']).expanduser() / '_templates'
        self.env = Environment(loader=FileSystemLoader(str(self.template_path)))
    

    def get_variables(self):
        now = datetime.now()
        today = date.today()
        vars = {
            'now': now,
            'today_iso': today.isoformat(),
            'now_iso': now.isoformat(timespec='seconds'),
            'today_long': today.strftime('%A, %B %d, %Y'),
            'now_long': now.strftime('%A, %B %d, %Y %I:%M %p')
        }
        vars.update(self.config.get('template_vars', {}))
        return vars

    def render_template(self, template_file, variables={}):
        template = self.env.get_template(template_file)
        return template.render(**variables)

    def create_file_from_template(self, template_file, output_file, extra_vars={}):
        vars = self.get_variables()
        vars.update(extra_vars)
        file_content = self.render_template(template_file, vars)
        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(file_content)

    def convert_key_value_vars_to_dict(self, var_list):
        """ Takes a list like ['foo=bar', 'bar=baz'] and converts it to {'foo': 'bar', 'bar': 'baz'} """
        vars = {}
        for var in var_list:
            key, value = self._parse_key_val_var(var)
            vars[key] = value
        return vars

    def _parse_key_val_var(self, var_str):
        """Takes a string in the format foo=bar and converts it to a tuple ('foo', 'bar')"""
        items = var_str.split('=')
        return (items[0].strip(), items[1].strip())
