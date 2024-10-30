#!/usr/bin/env python3
"""Module: 2-lifo_cache"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Caching system using LIFO algorithm"""

    def __init__(self):
        """ Initialize
        """
        self.recentlyAddedKey = None
        self.size = 0
        super().__init__()

    def put(self, key, value):
        """ Add an item in the cache"""
        if not key or not value:
            return
        # remove recently added key when cache is full
        if self.size >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
            print('DISCARD:', self.recentlyAddedKey)
            self.cache_data.pop(self.recentlyAddedKey)
            self.size -= 1
        # add key to cache
        self.cache_data[key] = value
        self.recentlyAddedKey = key
        self.size += 1

    def get(self, key):
        """ Get an item by key"""
        return self.cache_data.get(key)
