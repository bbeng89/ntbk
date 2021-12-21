"""Tests for log sub-commands"""

# 3rd party imports
import pytest
from freezegun import freeze_time


@freeze_time("2021-12-30")
def test_no_args_opens_today(dispatcher, ntbk_dir):
    """Test calling app without any args opens todays file"""
    expected_path = ntbk_dir / 'log/2021/12-december/2021-12-30/index.md'
    dispatcher.run([])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
    assert expected_path.parent.exists()

@freeze_time("2021-12-30")
def test_today_default_file(dispatcher, ntbk_dir):
    """Test 'today' arg opens todays file"""
    expected_path = ntbk_dir / 'log/2021/12-december/2021-12-30/index.md'
    dispatcher.run(['today'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
    assert expected_path.parent.exists()

@freeze_time("2021-01-01")
def test_today_other_file(dispatcher, ntbk_dir):
    """Test specifying a different file for 'today' command"""
    expected_path = ntbk_dir / 'log/2021/01-january/2021-01-01/test.md'
    dispatcher.run(['today', 'test'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
    assert expected_path.parent.exists()

@freeze_time("2021-07-20")
def test_yesterday_default_file(dispatcher, ntbk_dir):
    """Test 'yesterday' arg opens yesterday's file"""
    expected_path = ntbk_dir / 'log/2021/07-july/2021-07-19/index.md'
    dispatcher.run(['yesterday'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
    assert expected_path.parent.exists()

@freeze_time("2021-07-20")
def test_yesterday_other_file(dispatcher, ntbk_dir):
    """Test specifying a different file for 'yesterday' command"""
    expected_path = ntbk_dir / 'log/2021/07-july/2021-07-19/work.md'
    dispatcher.run(['yesterday', 'work'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
    assert expected_path.parent.exists()

@freeze_time("2020-02-15")
def test_tomorrow_default_file(dispatcher, ntbk_dir):
    """Test 'tomorrow' arg opens tomorrow's file"""
    expected_path = ntbk_dir / 'log/2020/02-february/2020-02-16/index.md'
    dispatcher.run(['tomorrow'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
    assert expected_path.parent.exists()

@freeze_time("2020-02-15")
def test_tomorrow_other_file(dispatcher, ntbk_dir):
    """Test specifying a different file for 'tomorrow' command"""
    expected_path = ntbk_dir / 'log/2020/02-february/2020-02-16/notes.md'
    dispatcher.run(['tomorrow', 'notes'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
    assert expected_path.parent.exists()

@freeze_time("2021-01-01")
def test_date_default_file(dispatcher, ntbk_dir):
    """Test 'date' arg opens specified date's index file"""
    expected_path = ntbk_dir / 'log/2020/03-march/2020-03-01/index.md'
    dispatcher.run(['date', '2020-03-01'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
    assert expected_path.parent.exists()

@freeze_time("2021-01-01")
def test_date_other_file(dispatcher, ntbk_dir):
    """Test specifying a different file for 'date' command"""
    expected_path = ntbk_dir / 'log/2021/03-march/2021-03-01/notes.md'
    dispatcher.run(['date', '2021-03-01', 'notes'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
    assert expected_path.parent.exists()

def test_non_iso_date_fails(dispatcher):
    """Test that date command requires date to be iso format"""
    with pytest.raises(SystemExit):
        dispatcher.run(['date', '01/01/2020'])
    dispatcher.filesystem.open_file_in_editor.assert_not_called()

@freeze_time("2021-01-01")
def test_finding_log_index_file(dispatcher, ntbk_dir, mocker):
    """Test using --find flag outputs path to the default log file"""
    mocker.patch('builtins.print')
    expected_path = ntbk_dir / 'log/2021/01-january/2021-01-01/index.md'
    dispatcher.run(['today', '--find'])
    print.assert_called_once_with(expected_path)

def test_finding_log_other_file(dispatcher, ntbk_dir, mocker):
    """Test using --find flag outputs path to the specified log file"""
    mocker.patch('builtins.print')
    expected_path = ntbk_dir / 'log/2021/01-january/2021-01-01/notes.md'
    dispatcher.run(['date', '2021-01-01', 'notes', '--find'])
    print.assert_called_once_with(expected_path)

@freeze_time("2021-01-01")
def test_finding_logdate(dispatcher, ntbk_dir, mocker):
    """Test using --find-dir flag outputs path to specified date"""
    mocker.patch('builtins.print')
    expected_path = ntbk_dir / 'log/2021/01-january/2021-01-01'
    dispatcher.run(['today', '--find-dir'])
    print.assert_called_once_with(expected_path)
