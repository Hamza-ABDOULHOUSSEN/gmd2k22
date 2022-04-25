import sqlite3

from drugbank.drugbank_index_query import drugbank_search
from hpo.hpo_index_query import hpo_search
from omim.omim_index_query import omim_search
from stitch.stitch_chemical_sources_index_query import stitch_chemical_sources_search
from stitch.stitch_br08303_index_query import stitch_br08303_search

'''
GLOBAL LISTS :
disease_list = [[occurrence, disease_name, source]
curing_drug_list = [[occurrence, drug_name, description, indication, toxicity, sources]]
side_effects_from_drug_list = [[occurrence, drug_name, description, indication, toxicity, sources]]
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
    return f"\"symptom : *{symptom}* OR synonym : *{symptom}* OR is_a : *{symptom}*\""

def correction_hpo_disease_label(label):
    if (len(label) > 0 and label[0]=='#'):
        label = label.split(" ", 1)[1]

    if (len(label) > 0 and ',' in label):
        label = label.split(",", 1)[0]

    if (len(label) > 0 and ';' in label):
        label = label.split(";", 1)[0]

    return label


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
        disease = correction_hpo_disease_label(disease)
        disease_list.append(disease)

    conn.commit()
    curs.close()

    return disease_list

def search_disease_from_symptom(symptom, disease_list):

    ## get symptoms
    hpo_query = create_hpo_query(symptom)
    content_hpo = hpo_search(hpo_query)

    ## complete symptoms

    ## Count lost items
    Total_hpo_count = len(content_hpo)
    count = 0

    for elem in content_hpo:
        hpo_id = elem[0]

        disease_list_from_hpo = get_diseases_from_hpo(hpo_id)

        if disease_list_from_hpo == []:
            count += 1
        else:
            for disease in disease_list_from_hpo:
                disease_list.append([symptom, disease, "hpo"])

    return disease_list

def complete_search(symptom):

    # correction of the input
    symptom = symptom.lower()

    # initiation of global lists
    disease_list = []
    curing_drug_list = []
    side_effects_from_drug_list = []

    disease_list = search_disease_from_symptom(symptom, disease_list)

    return disease_list, curing_drug_list, side_effects_from_drug_list

def main():
    symptom = "abdominal"

    # correction of the input
    symptom = symptom.lower()

    # initiation of global lists
    disease_list = []
    curing_drug_list = []
    side_effects_from_drug_list = []

    disease_list = search_disease_from_symptom(symptom, disease_list)

    print(len(disease_list))
    printlist(disease_list)

if __name__ == '__main__':
    main()