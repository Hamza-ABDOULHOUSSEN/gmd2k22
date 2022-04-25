from drugbank.drugbank_index_query import drugbank_search
from hpo.hpo_index_query import hpo_search
from omim.omim_index_query import omim_search
from stitch.stitch_chemical_sources_index_query import stitch_chemical_sources_search
from stitch.stitch_br08303_index_query import stitch_br08303_search

def replace1m(text):
    text = ""
    return text
    ## CID1... to CIDm...

def replace0s(text):
    text = ""
    return text
    ## CID0... to CIDs...

def sider_to_stitch_compoundid1(id1, id2):
    table = []
    return table
    # retourne la liste des source_code


def stitch_source_code_to_stitch_atc_code(code):
    table = []
    return table
    # retourne la liste des atc_code

def stitch_atc_code_to_drugbank(atc_code):
    table = []
    return table
    # retourne les listes [[name, description, ...]]