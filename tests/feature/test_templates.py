from freezegun import freeze_time

@freeze_time('2021-01-01')
def test_creating_new_log_with_default_template(dispatcher, ntbk_dir, simple_template):
    t_name = simple_template.get_name()
    dispatcher.config.set('default_templates', {'log': { 'index': t_name }})
    expected_file = ntbk_dir / 'log/2021/01-january/2021-01-01/index.md'
    dispatcher.run(['today'])
    assert expected_file.read_text() == '# Simple Template'
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_file)

def test_creating_new_collection_with_default_template(dispatcher, ntbk_dir, simple_template):
    t_name = simple_template.get_name()
    dispatcher.config.set('default_templates', {'collection': { 'books': t_name }})
    expected_file = ntbk_dir / 'collections/books/1984.md'
    dispatcher.run(['collection', 'books', '1984'])
    assert expected_file.read_text() == '# Simple Template'
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_file)

def test_non_empty_file_not_overwritten():
    pass

def test_creating_log_with_template_arg():
    pass

def test_creating_collection_with_template_arg():
    pass

def test_config_template_variables():
    pass

def test_var_arg_variables():
    pass