import pytest
from omim.omim_index_query import omim_search
import sys

def test_search():
    query = "\"omim_id : 100300\""

    argc = len(sys.argv)
    if (argc > 1):
        query = sys.argv[1]
        query = f'"{query}"'

    content = omim_search(query)
    assert(len(content) == 1)
