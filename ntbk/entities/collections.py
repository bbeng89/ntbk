class Collection():
    def __init__(self, config, filesystem, name):
        self.config = config
        self.filesystem = filesystem
        self.name = name

    def get_path(self):
        return self.filesystem.get_collection_base_path() / self.name

    def has_default_template(self):
        return self.get_default_template_name is not None

    def get_default_template_name(self):
        return self.config.get('default_templates', {}).get('collection', {}).get(self.name, None)

class CollectionFile():
    def __init__(self, config, filesystem, collection, filename):
        self.config = config
        self.collection = Collection(config, filesystem, collection)
        self.filename = filename

    def get_path(self):
        return self.collection.get_path() / self.filename

    