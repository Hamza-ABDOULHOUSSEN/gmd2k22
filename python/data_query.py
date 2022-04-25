import sqlite3

from drugbank.drugbank_index_query import drugbank_search
from hpo.hpo_index_query import hpo_search
from omim.omim_index_query import omim_search
from stitch.stitch_chemical_sources_index_query import stitch_chemical_sources_search
from stitch.stitch_br08303_index_query import stitch_br08303_search

'''
GLOBAL LISTS :
disease_list = [[occurrence, disease_name]
curing_drug_list = [[occurrence, drug_name, description, indication, toxicity, sources, lost]]
side_effects_from_drug_list = [[occurrence, drug_name, description, indication, toxicity, sources, lost]]
'''

# GLOBAL LISTS
disease_list = []
curing_drug_list = []
side_effects_from_drug_list = []

# temp just to print and check values
def printlist(output):
    for item in output:
        print(item)

def create_drugbank_query(symptom):
    return f"\"description : *{symptom}*\""

def create_hpo_query(symptom):
    return f"\"symptom : *{symptom}*\""

def get_diseases_from_hpo(hpo_id):

    disease_list = []

    DATABASE = "../data/HPO/hpo_annotations.sqlite"
    conn = sqlite3.connect(DATABASE)
    curs = conn.cursor()

    hpo_id = hpo_id.replace('_', ':')

    req = f"SELECT disease_label FROM phenotype_annotation WHERE sign_id = \"{hpo_id}\""
    curs.execute(req)

    for disease_tuple in curs.fetchall():
        disease = disease_tuple[0]
        disease = disease.lower()
        disease_list.append(disease)

    conn.commit()
    curs.close()

    return disease_list

def search_from_symptom(symptom):
    symptom = symptom.lower()
    output = []

    ## get symptoms
    hpo_query = create_hpo_query(symptom)
    content_hpo = hpo_search(hpo_query)

    ## complete symptoms
    for elem in content_hpo:
        hpo_id = elem[0]

        disease_list = get_diseases_from_hpo(hpo_id)

        if disease_list == []:
            output.append([symptom, ""])
        else:
            for disease in disease_list:
                output.append([symptom, disease])

    return output

def complete_search(symptom):

    # correction of the input

    # initiation of global lists
    disease_list = []
    curing_drug_list = []
    side_effects_from_drug_list = []

def main():
    REQUEST = "sepsis"
    REQUEST = "abdominal"

    output = search_from_symptom(REQUEST)

    printlist(output)


if __name__ == '__main__':
    main()