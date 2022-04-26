import sqlite3
import pandas as pd

from drugbank.drugbank_index_query import drugbank_search
from hpo.hpo_index_query import hpo_search
from omim.omim_index_query import omim_search
from stitch.stitch_chemical_sources_index_query import stitch_chemical_sources_search
from stitch.stitch_br08303_index_query import stitch_br08303_search

from python_requests import *
from usefull_temp import *
from link import *

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

## SEARCH FROM HPO
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

## SEARCH FROM SIDER

SIDER_FILE = "../data/MEDDRAS/meddra_all_se2.csv"

def get_sider_id(symptom):
    content = []
    df = pd.read_csv(SIDER_FILE, sep=',')
    n = len(df)

    for k in range(n):
        if symptom in df['side_effect_name'][k].lower():
            id1 = df['stitch_compound_id1'][k]
            id2 = df['stitch_compound_id2'][k]
            content.append([id1, id2])

    return content



## GLOBAL SEARCH FUNCTION

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

def search_side_effects_drug_from_symptom(symptom, side_effects_from_drug_list):

    ## get symptoms
    content_sider_id = get_sider_id(symptom)

    if len(content_sider_id) > 100:
        content_sider_id = content_sider_id[:100]

    ## link with stitch
    content_stitch_atc = []
    for elem in content_sider_id:
        id1 = elem[0]
        id2 = elem[1]
        content_stitch_atc += sider_to_stitch_compoundid1(id1, id2)

    if len(content_stitch_atc) > 500:
        content_stitch_atc = content_stitch_atc[:500]

    ## link with drugbank
    content_drugbank = []
    for atc_code in content_stitch_atc:
        content_drugbank += stitch_atc_code_to_drugbank(atc_code)

    allready_add_name_occurence = {}
    allready_add_name_item = {}
    for item in content_drugbank:
        name = item[0]

        if name in allready_add_name_occurence:
            allready_add_name_occurence[name] += 1
        else:
            description = item[1]
            indication = item[2]
            toxicity = item[3]
            bloc = [description, indication, toxicity, 'sider / stitch / drugbank']
            allready_add_name_item[name] = bloc
            allready_add_name_occurence[name] = 0


    allready_add_name_occurence = dict(sorted(allready_add_name_occurence.items(), key=lambda item: item[1], reverse=True))

    for name in allready_add_name_occurence:
        bloc = allready_add_name_item[name]
        occurence = allready_add_name_occurence[name]
        description = bloc[0]
        indication = bloc[1]
        toxicity = bloc[2]
        source = bloc[3]
        side_effects_from_drug_list.append([occurence, name, description, indication, toxicity, source])

    return side_effects_from_drug_list

def complete_search(symptom):

    # correction of the input
    symptom = symptom.lower()

    # initiation of global lists
    disease_list = []
    curing_drug_list = []
    side_effects_from_drug_list = []

    disease_list = search_disease_from_symptom(symptom, disease_list)
    side_effects_from_drug_list = search_side_effects_drug_from_symptom(symptom, side_effects_from_drug_list)

    return disease_list, curing_drug_list, side_effects_from_drug_list

def main():
    symptom = "abdominal"

    # correction of the input
    symptom = symptom.lower()

    #stitch_compound_id1
    #stitch_compound_id2
    #side_effect_name

    # initiation of global lists
    disease_list = []
    curing_drug_list = []
    side_effects_from_drug_list = []

    #disease_list = search_disease_from_symptom(symptom, disease_list)
    '''
    content_sider_id = [['CID100000085', 'CID000010917'], ['CID100000085', 'CID000010917'], ['CID100000085', 'CID000010917'], ['CID100000085', 'CID000010917'], ['CID100000143', 'CID000149436'], ['CID100000143', 'CID000149436'], ['CID100000143', 'CID000149436'], ['CID100000143', 'CID000149436'], ['CID100000143', 'CID000149436'], ['CID100000143', 'CID000149436'], ['CID100000143', 'CID000149436'], ['CID100000143', 'CID000149436'], ['CID100000158', 'CID005280360'], ['CID100000158', 'CID005280360'], ['CID100000159', 'CID005282411'], ['CID100000159', 'CID005282411'], ['CID100000159', 'CID005282411'], ['CID100000159', 'CID005282411'], ['CID100000159', 'CID005282411'], ['CID100000159', 'CID005282411'], ['CID100000159', 'CID005282411'], ['CID100000160', 'CID005280363'], ['CID100000160', 'CID005280363'], ['CID100000191', 'CID000060961'], ['CID100000191', 'CID000060961'], ['CID100000191', 'CID000060961'], ['CID100000214', 'CID005280723'], ['CID100000214', 'CID005280723'], ['CID100000247', 'CID000000247'], ['CID100000247', 'CID000000247'], ['CID100000298', 'CID000005959'], ['CID100000298', 'CID000005959'], ['CID100000311', 'CID000000311'], ['CID100000311', 'CID000000311'], ['CID100000311', 'CID000000311'], ['CID100000311', 'CID000000311'], ['CID100000312', 'CID000000312'], ['CID100000312', 'CID000000312'], ['CID100000338', 'CID000000338'], ['CID100000338', 'CID000000338'], ['CID100000444', 'CID000000444'], ['CID100000444', 'CID000000444'], ['CID100000444', 'CID000000444'], ['CID100000444', 'CID000000444'], ['CID100000444', 'CID000000444'], ['CID100000444', 'CID000000444'], ['CID100000444', 'CID000000444'], ['CID100000444', 'CID000000444'], ['CID100000444', 'CID000000444'], ['CID100000444', 'CID000000444'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000450', 'CID000005757'], ['CID100000453', 'CID000006251'], ['CID100000453', 'CID000006251'], ['CID100000564', 'CID000000564'], ['CID100000564', 'CID000000564'], ['CID100000596', 'CID000006252'], ['CID100000596', 'CID000006252'], ['CID100000598', 'CID000000598'], ['CID100000598', 'CID000000598'], ['CID100000598', 'CID000000598'], ['CID100000598', 'CID000000598'], ['CID100000598', 'CID000000598'], ['CID100000698', 'CID000005870'], ['CID100000698', 'CID000005870'], ['CID100000698', 'CID000005870'], ['CID100000698', 'CID000005870'], ['CID100000699', 'CID003001028'], ['CID100000699', 'CID003001028'], ['CID100000699', 'CID003001028'], ['CID100000699', 'CID003001028'], ['CID100000699', 'CID003001028'], ['CID100000699', 'CID003001028'], ['CID100000738', 'CID000005961'], ['CID100000738', 'CID000005961'], ['CID100000738', 'CID000005961'], ['CID100000767', 'CID000000767'], ['CID100000767', 'CID000000767'], ['CID100000767', 'CID000000767'], ['CID100000767', 'CID000000767'], ['CID100000767', 'CID000000767'], ['CID100000774', 'CID000000774'], ['CID100000774', 'CID000000774'], ['CID100000774', 'CID000000774']]

    content_stitch_atc = []
    for elem in content_sider_id:
        id1 = elem[0]
        id2 = elem[1]
        content_stitch_atc += sider_to_stitch_compoundid1(id1, id2)     
    '''

    side_effects_from_drug_list = search_side_effects_drug_from_symptom(symptom, side_effects_from_drug_list)

    print(len(side_effects_from_drug_list))
    printlist(side_effects_from_drug_list)

if __name__ == '__main__':
    main()