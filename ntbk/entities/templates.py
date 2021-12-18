# system imports
from pathlib import Path
from datetime import date, datetime

# 3rd party imports
from jinja2 import Environment, FileSystemLoader


class Template():
    def __init__(self, config, filesystem, name):
        self.config = config
        self.filesystem = filesystem
        self.template_path = self.filesystem.get_templates_base_path()
        self.env = Environment(loader=FileSystemLoader(str(self.template_path)))
        self.name = name

    def get_path(self):
        return self.filesystem.get_templates_base_path() / self.name

    def render(self, extra_vars={}):
        vars = dict(self.get_variables())
        vars.update(extra_vars)
        template = self.env.get_template(self.name)
        return template.render(**vars)

    # def create_file(self, output_file, extra_vars={}):
    #     vars = dict(self.get_variables())
    #     vars.update(extra_vars)
    #     file_content = self.render(vars)
    #     out_path = Path(output_file)
    #     out_path.parent.mkdir(parents=True, exist_ok=True)
    #     out_path.write_text(file_content)

    def get_default_variables(self):
        now = datetime.now()
        today = date.today()
        return {
            'now': now,
            'today_iso': today.isoformat(),
            'now_iso': now.isoformat(timespec='seconds'),
            'today_long': today.strftime('%A, %B %d, %Y'),
            'now_long': now.strftime('%A, %B %d, %Y %I:%M %p')
        }
    
    def get_config_variables(self):
        return self.config.get('template_vars', {})

    def get_variables(self):
        vars = dict(self.get_default_variables())
        vars.update(self.get_config_variables())
        return vars

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




    


