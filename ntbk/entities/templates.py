# system imports
from pathlib import Path
from datetime import date, datetime

# 3rd party imports
from jinja2 import Environment, FileSystemLoader


class Template():
    """This class represents a template file in the _templates directory. It knows how to render itself using Jinja2"""

    EXTENSION = '.md'
    extra_vars = {}

    def __init__(self, config, filesystem, name):
        self.config = config
        self.filesystem = filesystem
        self.template_path = self.filesystem.get_templates_base_path()
        self.env = Environment(loader=FileSystemLoader(str(self.template_path)))
        self.name = name

    def get_path(self):
        """Get the pathlib.Path object for this template"""
        return self.filesystem.get_templates_base_path() / self.name

    def get_name(self):
        """Get the string name of this template"""
        return self.name

    def render(self, extra_vars={}):
        """Render this template with jinja2 and return the resulting template as a string"""
        vars = dict(self.get_variables())
        vars.update(extra_vars)
        template = self.env.get_template(self.name + self.EXTENSION)
        return template.render(**vars)

    def set_extra_vars(self, vars):
        """Set extra variables to be sent to the template when its rendered"""
        self.extra_vars = vars
    
    def get_default_variables(self):
        """Get the global default variables available to all templates"""
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
        """Get the variables that are defined in the config file"""
        return self.config.get('template_vars', {}) or {}

    def get_variables(self):
        """Get a dict of all variables to be passed to the template"""
        vars = dict(self.get_default_variables())
        vars.update(self.get_config_variables())
        vars.update(self.extra_vars)
        return vars


# Top-level function to list all templates
def get_all_templates(config, filesystem):
    """Get a list of Template objects for all templates in the notebook"""
    return [Template(config, filesystem, child.stem) for child in filesystem.get_templates_base_path().glob('*.md')]

