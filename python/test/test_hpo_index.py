import pytest
from hpo.hpo_index_query import hpo_search

def test_search():
    #content = stitch_chemical_sources_search('"source_format : ATC"')
    #assert(len(content) == 10)

    content = hpo_search('"* : *"')
    assert(len(content) == 12299)
