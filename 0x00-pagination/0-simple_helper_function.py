#!/usr/bin/env python3
"""Module: 0-simple_helper_function"""


def index_range(page: int, page_size: int):
    """Returns a tuple containing the start and end index
    corresponding to the range of indexes to return in a list
    for those particular pagination parameters.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index
