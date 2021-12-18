# app imports
from templates import Template


class Collection():
    def __init__(self, config, filesystem, name):
        self.config = config
        self.filesystem = filesystem
        self.name = name

    def get_path(self):
        return self.filesystem.get_collection_base_path() / self.name

    def get_name(self):
        return self.name

    def has_default_template(self):
        return self.get_default_template_name is not None

    def get_default_template_name(self):
        return self.config.get('default_templates', {}).get('collection', {}).get(self.name, None)

    def get_default_template(self):
        if not self.has_default_template():
            return None
        return Template(self.config, self.filesystem, self.get_default_template_name())

    def get_files(self):
        return [CollectionFile(self.config, self.filesystem, self.name, child.stem) for child in self.get_path().glob('*.md')]

    def get_file_count(self):
        return len(self.get_files())

class CollectionFile():

    EXTENSION = '.md'

    def __init__(self, config, filesystem, collection_name, filename):
        self.config = config
        self.collection = Collection(config, filesystem, collection_name)
        self.filename = filename

    def get_path(self):
        return self.collection.get_path() / f'{self.filename}{self.EXTENSION}'

    def get_name(self):
        return self.filename

    def has_default_template(self):
        return self.collection.has_default_template()

    def get_default_template_name(self):
        return self.collection.get_default_template_name()

    def get_default_template(self):
        return self.collection.get_default_template()


# Top-level function to list all collections
def get_all_collections(config, filesystem):
    return [Collection(config, filesystem, child.stem) for child in filesystem.get_collection_base_path().glob('*/')]
        