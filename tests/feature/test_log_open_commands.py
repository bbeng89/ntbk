# 3rd party imports
import pytest
from freezegun import freeze_time

# app imports
from ntbk.dispatcher import Dispatcher


@freeze_time("2021-12-30")
def test_no_args_opens_today(dispatcher, ntbk_dir):
    expected_path = ntbk_dir / 'log/2021/12-december/2021-12-30/index.md'
    dispatcher.run([])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)

@freeze_time("2021-12-30")
def test_today_default_file(dispatcher, ntbk_dir):
    expected_path = ntbk_dir / 'log/2021/12-december/2021-12-30/index.md'
    dispatcher.run(['today'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
    
@freeze_time("2021-01-01")
def test_today_other_file(dispatcher, ntbk_dir):
    expected_path = ntbk_dir / 'log/2021/01-january/2021-01-01/test.md'
    dispatcher.run(['today', 'test'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)

@freeze_time("2021-07-20")
def test_yesterday_default_file(dispatcher, ntbk_dir):
    expected_path = ntbk_dir / 'log/2021/07-july/2021-07-19/index.md'
    dispatcher.run(['yesterday'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)

@freeze_time("2021-07-20")
def test_yesterday_other_file(dispatcher, ntbk_dir):
    expected_path = ntbk_dir / 'log/2021/07-july/2021-07-19/work.md'
    dispatcher.run(['yesterday', 'work'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)

@freeze_time("2020-02-15")
def test_tomorrow_default_file(dispatcher, ntbk_dir):
    expected_path = ntbk_dir / 'log/2020/02-february/2020-02-16/index.md'
    dispatcher.run(['tomorrow'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)

@freeze_time("2020-02-15")
def test_tomorrow_other_file(dispatcher, ntbk_dir):
    expected_path = ntbk_dir / 'log/2020/02-february/2020-02-16/notes.md'
    dispatcher.run(['tomorrow', 'notes'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)

@freeze_time("2021-01-01")
def test_date_default_file(dispatcher, ntbk_dir):
    expected_path = ntbk_dir / 'log/2020/03-march/2020-03-01/index.md'
    dispatcher.run(['date', '2020-03-01'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)

@freeze_time("2021-01-01")
def test_date_other_file(dispatcher, ntbk_dir):
    expected_path = ntbk_dir / 'log/2021/03-march/2021-03-01/notes.md'
    dispatcher.run(['date', '2021-03-01', 'notes'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)

def test_non_iso_date_fails(dispatcher):
    with pytest.raises(SystemExit):
        dispatcher.run(['date', '01/01/2020'])
    dispatcher.filesystem.open_file_in_editor.assert_not_called()
