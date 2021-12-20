from ntbk.config import Config
import ntbk.initialize

# TODO - need to test dispatching a normal command and making sure the init procedures run

def test_initializing_config_file(tmp_path, mocker):
    # mock the user input prompts - return ~/ntbk for the first prompt, and vim for the second
    mocker.patch('builtins.input', side_effect=['~/ntbk', 'vim'])
    config_file = tmp_path / 'ntbk.yml'
    conf = Config(file_path=config_file)
    ntbk.initialize.init_config_file(conf)
    assert config_file.exists()
    assert conf.get('ntbk_dir') == '~/ntbk'
    assert conf.get('editor') == 'vim'

def test_initializing_notebook():
    # TODO - make sure user is prompted for ntbk path and editor and ntbk is created
    pass