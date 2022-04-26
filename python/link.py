from drugbank.drugbank_index_query import drugbank_search
from hpo.hpo_index_query import hpo_search
from omim.omim_index_query import omim_search
from stitch.stitch_chemical_sources_index_query import stitch_chemical_sources_search
from stitch.stitch_br08303_index_query import stitch_br08303_search

def sider_to_stitch_compoundid1(id1, id2):
    ida = id1.replace('1', 'm', 1)
    idb = id2.replace('0', 's', 1)
    query = f'"chemical : {ida}"'
    table = stitch_chemical_sources_search(query)
    result = []
    for elem in table:
        result.append(elem[3])
    return result
    # retourne la liste des source_code

def stitch_source_code_to_stitch_atc_code(code):
    query = f'"atc_code : {code}"'
    table = stitch_br08303_search(query)
    result = []
    for elem in table:
        result.append(elem[1])
    return result
    # retourne la liste des atc_code

def stitch_atc_code_to_drugbank(atc_code):
    query = f'"atc_code : {atc_code}"'
    table = drugbank_search(query)
    result = []
    for elem in table:
        result.append([elem[1], elem[2], elem[3], elem[4]])
    return result
    # retourne les listes [[name, description, ...]]