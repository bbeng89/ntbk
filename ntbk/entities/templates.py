# system imports
from pathlib import Path
from datetime import date, datetime

# 3rd party imports
from jinja2 import Environment, FileSystemLoader


class Template():
    extra_vars = {}

    def __init__(self, config, filesystem, name):
        self.config = config
        self.filesystem = filesystem
        self.template_path = self.filesystem.get_templates_base_path()
        self.env = Environment(loader=FileSystemLoader(str(self.template_path)))
        self.name = name

    def get_path(self):
        return self.filesystem.get_templates_base_path() / self.name

    def get_name(self):
        return self.name

    def render(self, extra_vars={}):
        vars = dict(self.get_variables())
        vars.update(extra_vars)
        template = self.env.get_template(self.name)
        return template.render(**vars)

    def set_extra_vars(self, vars):
        self.extra_vars = vars
    
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
        vars.update(self.extra_vars)
        return vars


# Top-level function to list all templates
def get_all_templates(config, filesystem):
    return [Template(config, filesystem, child.stem) for child in filesystem.get_templates_base_path().glob('*.md')]

