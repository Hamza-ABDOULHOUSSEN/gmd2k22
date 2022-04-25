import pytest
from hpo.hpo_index_query import hpo_search
import sys

def test_search():
    #content = stitch_chemical_sources_search('"source_format : ATC"')
    #assert(len(content) == 10)

    content = hpo_search('"* : *"')
    assert(len(content) == 12299)

    query = "\"hpo_id : HP_0000050\""

    argc = len(sys.argv)
    if (argc > 1):
        query = sys.argv[1]
        query = f'"{query}"'

    assert(len(query) == 24)
