
def test_opening_collection_default_file(dispatcher, ntbk_dir):
    expected_path = ntbk_dir / 'collections/books/index.md'
    dispatcher.run(['collection', 'books'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)

def test_opening_collection_other_file(dispatcher, ntbk_dir):
    expected_path = ntbk_dir / 'collections/books/dune.md'
    dispatcher.run(['collection', 'books', 'dune'])
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_path)
