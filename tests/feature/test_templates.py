from freezegun import freeze_time

@freeze_time('2021-01-01')
def test_creating_new_log_with_default_template(dispatcher, ntbk_dir, template_factory):
    template = template_factory()
    dispatcher.config.set('default_templates', {'log': { 'index': template.get_name() }})
    expected_file = ntbk_dir / 'log/2021/01-january/2021-01-01/index.md'
    dispatcher.run(['today'])
    assert expected_file.read_text() == template.render()
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_file)

def test_creating_new_collection_with_default_template(dispatcher, ntbk_dir, template_factory):
    template = template_factory()
    dispatcher.config.set('default_templates', {'collection': { 'books': template.get_name() }})
    expected_file = ntbk_dir / 'collections/books/1984.md'
    dispatcher.run(['collection', 'books', '1984'])
    assert expected_file.read_text() == template.render()
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_file)

# Eventually I'd like to make it actually overwrite files that are empty (newlines and spaces wouldnt count as content)
def test_existing_file_not_overwritten(dispatcher, collection_file, template_factory):
    template = template_factory()
    c_name = collection_file.get_collection().get_name()
    dispatcher.config.set('default_templates', {'collection': { c_name: template.get_name() }})
    collection_file.get_path().write_text('Placeholder text')
    dispatcher.run(['collection', c_name, collection_file.get_name()])
    # make sure the existing text is not overwritten by the default template
    assert collection_file.get_path().read_text() == 'Placeholder text'
    dispatcher.filesystem.open_file_in_editor.assert_called_with(collection_file.get_path())

@freeze_time('2021-01-01')
def test_creating_log_with_template_arg(dispatcher, ntbk_dir, template_factory):
    template = template_factory()
    expected_file = ntbk_dir / 'log/2021/01-january/2021-01-01/index.md'
    dispatcher.run(['today', '--template', template.get_name()])
    assert expected_file.read_text() == template.render()
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_file)

def test_creating_collection_with_template_arg(dispatcher, ntbk_dir, template_factory):
    template = template_factory()
    expected_file = ntbk_dir / 'collections/books/1984.md'
    dispatcher.run(['collection', 'books', '1984', '--template', template.get_name()])
    assert expected_file.read_text() == template.render()
    dispatcher.filesystem.open_file_in_editor.assert_called_with(expected_file)

def test_standard_variables_replaced():
    pass

def test_config_template_variables():
    pass

def test_var_arg_variables():
    pass