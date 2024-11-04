#!/usr/bin/env python3
"""Module: 2-lifo_cache"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """Caching system using LFU algorithm"""

    def __init__(self):
        """ Initialize
        """
        self.lfu = {}
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache"""
        if key is None or item is None:
            return
        if len(self.lfu) == BaseCaching.MAX_ITEMS:
            if key not in self.cache_data:
                min_key = min(self.lfu, key=self.lfu.get)
                print('DISCARD:', min_key)
                self.lfu.pop(min_key)
                self.cache_data.pop(min_key)
        if key not in self.lfu:
            self.lfu[key] = 0
        else:
            self.lfu[key] += 1
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key"""
        if key in self.cache_data:
            self.lfu[key] += 1

        return self.cache_data.get(key)
