import sys
sys.path.append('../python')

from drugbank.drugbank_index_query import *

def drugbank_query(query):
    return drugbank_search(query)
