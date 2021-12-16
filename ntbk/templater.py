import config
from pathlib import Path
from datetime import date, datetime
from jinja2 import Environment, FileSystemLoader

class Templater():

    def __init__(self):
        self.config = config.load_config()
        self.template_path = Path(self.config['ntbk_dir']).expanduser() / '_templates'
        self.env = Environment(loader=FileSystemLoader(str(self.template_path)))

    def get_standard_template_variables(self):
        now = datetime.now()
        today = date.today()
        return {
            'now': now,
            'today_iso': today.isoformat(),
            'now_iso': now.isoformat(timespec='seconds'),
            'today_long': today.strftime('%A, %B %d, %Y'),
            'now_long': now.strftime('%A, %B %d, %Y %I:%M %p')
        }

    def render_template(self, template_file, variables={}):
        template = self.env.get_template(template_file)
        return template.render(**variables)

    def create_file_from_template(self, template_file, output_file, extra_vars={}):
        vars = self.get_standard_template_variables()
        vars.update(extra_vars)
        file_content = self.render_template(template_file, vars)
        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(file_content)
