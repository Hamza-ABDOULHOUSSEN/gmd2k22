from drugbank.drugbank_index_query import drugbank_search
from hpo.hpo_index_query import hpo_search
from omim.omim_index_query import omim_search
from stitch.stitch_chemical_sources_index_query import stitch_chemical_sources_search
from stitch.stitch_br08303_index_query import stitch_br08303_search

def replace1m(text): # CID1... to CIDm...
    text = str(text)
    text = text[0:3] + "m" + text[4:]
    return text

def replace0s(text): # CID0... to CIDs...
    text = str(text)
    text = text[0:3] + "s" + text[4:]
    return text

def sider_to_stitch_compoundid1(id1, id2):
    ida = replace1m(id1)
    idb = replace0s(id2)
    query = '"chemical : ' + ida + ' OR chemical : ' + idb + '"'
    table = stitch_chemical_sources_search(query)
    print(table)
    # retourne la liste des source_code

def stitch_source_code_to_stitch_atc_code(code):
    table = []
    return table
    # retourne la liste des atc_code

def stitch_atc_code_to_drugbank(atc_code):
    table = []
    return table
    # retourne les listes [[name, description, ...]]

sider_to_stitch_compoundid1("CID100003269","CID000005756")
