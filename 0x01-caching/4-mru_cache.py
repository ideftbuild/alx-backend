#!/usr/bin/env python3
"""Module: 2-lifo_cache"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """Caching system using LRU algorithm"""

    def __init__(self):
        """ Initialize
        """
        self.mru = []
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache"""
        if key is None or item is None:
            return
        if len(self.mru) == BaseCaching.MAX_ITEMS:
            if key not in self.mru:
                mru = self.mru[-1]
                print('DISCARD:', mru)
                self.mru.pop(-1)
                self.cache_data.pop(mru)
            else:
                self.mru.remove(key)

        self.mru.append(key)
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key"""
        if key in self.cache_data and key != self.mru[:-1]:
            # move key to the end of the list
            self.mru.remove(key)
            self.mru.append(key)
        return self.cache_data.get(key)
