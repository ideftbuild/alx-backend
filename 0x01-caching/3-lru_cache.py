#!/usr/bin/env python3
"""Module: 2-lifo_cache"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """Caching system using LRU algorithm"""

    def __init__(self):
        """ Initialize
        """
        self.lru = []
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache"""
        if key is None or item is None:
            return
        if len(self.lru) == BaseCaching.MAX_ITEMS:
            lru = self.lru[0]
            print('DISCARD:', lru)
            self.lru.pop(0)
            self.cache_data.pop(lru)

        self.lru.append(key)
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key"""
        if key in self.cache_data and key != self.lru[:-1]:
            # move key to the end of the list
            self.lru.remove(key)
            self.lru.append(key)
        return self.cache_data.get(key)
