from unittest import TestCase
from flask import Flask, current_app

import mock

__author__ = 'andi'

from cache import Cache


class CacheTest(Cache):

    def __init__(self):
        super(CacheTest, self).__init__()
        self.item = mock.Mock()

    def get_item_name(self):
        return 'foo'

    def generate_item(self):
        return self.item


class TestCache(TestCase):

    def setUp(self):
        self.cache_mock = mock.Mock()

        self.app = Flask(__name__)
        with self.app.app_context():
            current_app.config['cache'] = self.cache_mock

            self.cache = CacheTest()

    def test_get_item_name(self):
        self.assertEqual('foo', self.cache.get_item_name())

    def test_get_item_not_in_cache(self):

        self.cache_mock.get.return_value = None

        with self.app.app_context():

            item = self.cache.get_item()

            self.assertEqual(item, self.cache.item)
            self.assertEqual(1, self.cache_mock.set.call_count)
            self.cache_mock.set.assert_any_call('foo', self.cache.item, timeout=60)

    def test_get_item_not_in_cache(self):

        cached_item = mock.Mock()

        self.cache_mock.get.return_value = cached_item

        with self.app.app_context():
            item = self.cache.get_item()

            self.assertEqual(cached_item, item)
            self.assertEqual(0, self.cache_mock.set.call_count)
