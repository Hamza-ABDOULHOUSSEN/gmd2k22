import sys

sys.path.append('../python')
from data_query import *

from drugbank.drugbank_index_query import *

def drugbank_query(query):
    return drugbank_search(query)

def complete_search(symptom, content_sider_id):

    # correction of the input
    symptom = symptom.lower()

    # initiation of global lists
    disease_list = []
    curing_drug_list = []
    side_effects_from_drug_list = []

    disease_list = search_disease_from_symptom(symptom, disease_list)
    curing_drug_list = search_curing_drug_from_symtom(symptom, curing_drug_list)

    side_effects_from_drug_list = search_side_effects_drug_from_content_sider_id(content_sider_id, side_effects_from_drug_list)

    return disease_list, curing_drug_list, side_effects_from_drug_list