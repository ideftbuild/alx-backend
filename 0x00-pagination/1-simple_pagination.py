#!/usr/bin/env python3
"""Module: 1-simple_pagination"""

import csv
from typing import List


def index_range(page: int, page_size: int):
    """Returns a tuple containing the start and end index
    corresponding to the range of indexes to return in a list
    for those particular pagination parameters.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Get page"""
        try:
            assert page >= 1 and page_size >= 1
        except TypeError:
            raise AssertionError
        self.dataset()
        start, end = index_range(page, page_size)
        return self.__dataset[start:end]
