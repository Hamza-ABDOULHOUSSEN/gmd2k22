import sys

sys.path.append('../python')
from data_query import complete_search

from drugbank.drugbank_index_query import *

def drugbank_query(query):
    return drugbank_search(query)

def sb(query):
    disease_list, curing_drug_list, side_effects_from_drug_list = complete_search(query)
    return disease_list, curing_drug_list, side_effects_from_drug_list