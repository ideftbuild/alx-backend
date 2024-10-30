#!/usr/bin/env python3
"""Module: 1-fifo_cache"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """Caching system using FIFO algorithm"""

    def __init__(self):
        """Initialize"""
        self.size = 0
        super().__init__()


    def put(self, key, value):
        """ Add an item in the cache"""
        if not key or not value:
            return

        if self.size >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
            oldest_key = next(iter(self.cache_data))
            print('DISCARD:', oldest_key)
            self.cache_data.pop(oldest_key)
            self.size -= 1

        self.cache_data[key] = value
        self.size += 1

    def get(self, key):
        """ Get an item by key"""
        return self.cache_data.get(key)
