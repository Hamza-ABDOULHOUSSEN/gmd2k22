import pytest
from stitch.stitch_chemical_sources_index_query import stitch_chemical_sources_search

def test_search():
    #content = stitch_chemical_sources_search('"source_format : ATC"')
    #assert(len(content) == 10)

    content = stitch_chemical_sources_search('"source_code : M01AB10"')
    assert(len(content) == 1)
    assert(content[0][3] == "M01AB10")
    assert(content[0][0] == "CIDm00028871")
