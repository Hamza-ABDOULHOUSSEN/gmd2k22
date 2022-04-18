import pytest
from drugbank.drugbank_index_query import drugbank_search

def test_search():
    content = drugbank_search('"id : DB0000*"')
    assert(len(content) == 9)

    content = drugbank_search('"id : DB00001"')
    assert(len(content) == 1)
    assert(content[0][0] == "DB00001")
    assert(content[0][1] == "lepirudin")
