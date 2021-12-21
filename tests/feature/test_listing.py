"""Test listing templates, collections, and files"""
from unittest.mock import call
from colorama import Fore, Style
from freezegun import freeze_time

def test_listing_templates(dispatcher, filesystem, mocker):
    """Test 'templates' command lists all templates"""
    mocker.patch('builtins.print')
    template_path = filesystem.get_templates_base_path()
    template_path.mkdir(parents=True)
    (template_path / 'template_one.md').touch()
    (template_path / 'template_two.md').touch()

    dispatcher.run(['templates'])

    print.assert_has_calls([call('template_one'), call('template_two')], any_order=True)

def test_listing_collections(dispatcher, filesystem, mocker):
    """Test 'collections' command lists all collections"""
    aliases = ['collections', 'cols']
    mocker.patch('builtins.print')
    col_path = filesystem.get_collection_base_path()
    (col_path / 'books').mkdir(parents=True)
    (col_path / 'books' / 'index.md').touch()
    (col_path / 'recipes').mkdir(parents=True)
    (col_path / 'recipes' / 'chili.md').touch()
    (col_path / 'recipes' / 'lasagna.md').touch()

    for alias in aliases:
        dispatcher.run([alias])

        print.assert_has_calls([
            call(f'books {Fore.BLUE}[1 file]{Style.RESET_ALL}'),
            call(f'recipes {Fore.GREEN}[2 files]{Style.RESET_ALL}')],
            any_order=True)
        print.reset_mock()

@freeze_time("2020-01-01")
def test_listing_log_files_for_day(dispatcher, filesystem, mocker):
    """Test --list flag on log lists all files"""
    mocker.patch('builtins.print')
    log_base = filesystem.get_log_base_path()
    day_path = log_base / '2020/01-january/2020-01-01'
    day_path.mkdir(parents=True)
    (day_path / 'index.md').touch()
    (day_path / 'work.md').touch()

    dispatcher.run(['today', '--list'])

    print.assert_has_calls([call('index'), call('work')], any_order=True)

def test_listing_collection_files(dispatcher, filesystem, mocker):
    """test --list flag on collection lists all collection files"""
    mocker.patch('builtins.print')
    col_base = filesystem.get_collection_base_path()
    col_path = col_base / 'travel'
    col_path.mkdir(parents=True)
    (col_path / 'montana.md').touch()
    (col_path / 'utah.md').touch()

    dispatcher.run(['collection', 'travel', '--list'])

    print.assert_has_calls([call('montana'), call('utah')], any_order=True)
