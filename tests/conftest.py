from datetime import date
import pytest
from ntbk.config import Config
from ntbk.filesystem import Filesystem
from ntbk.dispatcher import Dispatcher
from ntbk.entities.logs import LogDate
from ntbk.entities.templates import Template

"""
This file is automatically loaded in every test by pytest.
See: https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files
"""

# 2021-12-30
FAKE_TODAY = date(2021, 12, 30)

@pytest.fixture
def config(tmp_path):
    return Config({ 
        'ntbk_dir': str(tmp_path),
        'default_templates': {},
        'template_vars': {}
        })

@pytest.fixture
def filesystem(config, mocker):
    fs = Filesystem(config)
    mocker.patch.object(fs, 'open_file_in_editor', autospec=True)
    return fs

@pytest.fixture
def dispatcher(config, filesystem):
    return Dispatcher(config, filesystem)

@pytest.fixture
def ntbk_dir(filesystem):
    return filesystem.get_notebook_base_path()

@pytest.fixture
def log_date(config, filesystem):
    d = date(2021, 1, 1)
    return LogDate(config, fileystem, d)

@pytest.fixture
def simple_template(config, filesystem):
    name = 'test_template'
    template_path = filesystem.get_templates_base_path()
    template_path.mkdir(parents=True, exist_ok=True)
    (template_path / (name + '.md')).write_text('# Simple Template')
    return Template(config, filesystem, 'test_template')

