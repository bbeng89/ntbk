import unittest.mock as mock
from freezegun import freeze_time
from ntbk.dispatcher import Dispatcher


@freeze_time("2021-12-30")
def test_no_args_opens_today(dispatcher):
    expected_path = dispatcher.filesystem.get_notebook_base_path() / 'log/2021/12-december/2021-12-30/index.md'
    dispatcher.run([])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)

@freeze_time("2021-12-30")
def test_today_default_file(dispatcher):
    expected_path = dispatcher.filesystem.get_notebook_base_path() / 'log/2021/12-december/2021-12-30/index.md'
    dispatcher.run(['today'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
    
@freeze_time("2021-01-01")
def test_today_other_file(dispatcher):
    expected_path = dispatcher.filesystem.get_notebook_base_path() / 'log/2021/01-january/2021-01-01/test.md'
    dispatcher.run(['today', 'test'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)


def test_yesterday_default_file():
    pass

def test_yesterday_other_file():
    pass

def test_tomorrow_default_file():
    pass

def test_tomorrow_other_file():
    pass

def test_date_default_file():
    pass

def test_date_other_file():
    pass

def test_list_files_for_day():
    pass

def test_create_file_from_template_args():
    pass

def test_create_file_from_default_template():
    pass

def test_jot():
    pass

def test_jot_with_timestamp():
    pass
