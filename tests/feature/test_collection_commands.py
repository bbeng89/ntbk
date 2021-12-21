"""Tests for 'collection' sub-commands"""

def test_opening_collection_default_file(dispatcher, ntbk_dir):
    """Test not specifying a file opens the index.md of a collection"""
    expected_path = ntbk_dir / 'collections/books/index.md'
    dispatcher.run(['collection', 'books'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
    assert expected_path.parent.exists()

def test_opening_collection_other_file(dispatcher, ntbk_dir):
    """Test not specifying file 'dune' opens the dune.md file of a collection"""
    expected_path = ntbk_dir / 'collections/books/dune.md'
    dispatcher.run(['collection', 'books', 'dune'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
    assert expected_path.parent.exists()

def test_finding_collection_index_file(dispatcher, ntbk_dir, mocker):
    """Test using the --find flag without a file name finds index.md"""
    mocker.patch('builtins.print')
    expected_path = ntbk_dir / 'collections/books/index.md'
    dispatcher.run(['collection', 'books', '--find'])
    print.assert_called_once_with(expected_path)

def test_finding_collection_other_file(dispatcher, ntbk_dir, mocker):
    """Test using the --find flag wit 'dune' file name finds dune.md"""
    mocker.patch('builtins.print')
    expected_path = ntbk_dir / 'collections/books/dune.md'
    dispatcher.run(['collection', 'books', 'dune', '--find'])
    print.assert_called_once_with(expected_path)

def test_finding_collection(dispatcher, ntbk_dir, mocker):
    """Test finding a collection directory"""
    mocker.patch('builtins.print')
    expected_path = ntbk_dir / 'collections/books'
    dispatcher.run(['collection', 'books', '--find-dir'])
    print.assert_called_once_with(expected_path)
