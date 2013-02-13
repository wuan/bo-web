from flask import current_app


class Cache(object):
    def __init__(self):
        self.cache = current_app.config['cache']

    def get_item(self):
        item = self.cache.get(self.get_item_name())

        if item is None:
            item = self.generate_item()
            self.cache.set(self.get_item_name(), item, timeout=60)

        return item

