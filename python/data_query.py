import sqlite3
import pandas as pd
import time
import sys

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

## SEARCH FROM DRUGBANK

## GLOBAL SEARCH FUNCTION

def search_disease_from_symptom(symptom, disease_list):

    ## get symptoms
    hpo_query = create_hpo_query(symptom)
    content_hpo = hpo_search(hpo_query)

    ## complete symptoms

    ## Count lost items
    Total_hpo_count = len(content_hpo)
    count = 0

    allready_add_name_occurence = {}

    for elem in content_hpo:
        hpo_id = elem[0]

        disease_list_from_hpo = get_diseases_from_hpo(hpo_id)

        if disease_list_from_hpo == []:
            count += 1
        else:
            for disease in disease_list_from_hpo:

                if disease in allready_add_name_occurence:
                    allready_add_name_occurence[disease] += 1
                else:
                    allready_add_name_occurence[disease] = 1

    allready_add_name_occurence = dict(sorted(allready_add_name_occurence.items(), key=lambda item: item[1], reverse=True))

    for disease in allready_add_name_occurence:
        occurrence = allready_add_name_occurence[disease]
        sources = "hpo"
        disease_list.append([occurrence, disease, sources])

    return disease_list

def search_side_effects_drug_from_symptom(symptom, side_effects_from_drug_list):

    ## get symptoms
    content_sider_id = get_sider_id(symptom)

    if len(content_sider_id) > 2:
        content_sider_id = content_sider_id[:2]

    ## link with stitch
    content_stitch_atc = []
    for elem in content_sider_id:
        id1 = elem[0]
        id2 = elem[1]
        content_stitch_atc += sider_to_stitch_compoundid1(id1, id2)

    if len(content_stitch_atc) > 100:
        content_stitch_atc = content_stitch_atc[:100]

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
            allready_add_name_occurence[name] = 1


    allready_add_name_occurence = dict(sorted(allready_add_name_occurence.items(), key=lambda item: item[1], reverse=True))

    for name in allready_add_name_occurence:
        bloc = allready_add_name_item[name]
        occurrence = allready_add_name_occurence[name]
        description = bloc[0]
        indication = bloc[1]
        toxicity = bloc[2]
        source = bloc[3]
        side_effects_from_drug_list.append([occurrence, name, description, indication, toxicity, source])

    return side_effects_from_drug_list

def search_side_effects_drug_from_content_sider_id(content_sider_id, side_effects_from_drug_list):

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
                allready_add_name_occurence[name] = 1

        allready_add_name_occurence = dict(
            sorted(allready_add_name_occurence.items(), key=lambda item: item[1], reverse=True))

        for name in allready_add_name_occurence:
            bloc = allready_add_name_item[name]
            occurrence = allready_add_name_occurence[name]
            description = bloc[0]
            indication = bloc[1]
            toxicity = bloc[2]
            source = bloc[3]
            side_effects_from_drug_list.append([occurrence, name, description, indication, toxicity, source])

        return side_effects_from_drug_list

def search_curing_drug_from_symtom(symptom, curing_drug_list):
    query = create_drugbank_query(symptom)
    content_drugbank = drugbank_search(query)

    allready_add_name_occurence = {}
    allready_add_name_item = {}
    for item in content_drugbank:
        name = item[1]

        if name in allready_add_name_occurence:
            allready_add_name_occurence[name] += 1
        else:
            description = item[2]
            indication = item[3]
            toxicity = item[4]
            sources = "drugbank"
            bloc = [description, indication, toxicity, sources]
            allready_add_name_item[name] = bloc
            allready_add_name_occurence[name] = 1

    allready_add_name_occurence = dict(sorted(allready_add_name_occurence.items(), key=lambda item: item[1], reverse=True))

    for name in allready_add_name_occurence:
        bloc = allready_add_name_item[name]
        occurrence = allready_add_name_occurence[name]
        description = bloc[0]
        indication = bloc[1]
        toxicity = bloc[2]
        sources = bloc[3]

        curing_drug_list.append([occurrence, name, description, indication, toxicity, sources])

    return curing_drug_list

def main():

    symptom = "abdominal"

    # correction of the input
    symptom = symptom.lower()

    ## THINGS TO PRINT : {0: disease_list, 1: curing_drug_list, 2: side_effects_from_drug_list, 3: All}
    print_value = 1

    ## CHECK ARGS
    args = sys.argv
    if "-s" in args:
        pos = args.index("-s")
        symptom = args[pos+1]
    if "-p" in args:
        pos = args.index("-p")
        print_value = int(args[pos+1])

    # initiation of global lists
    disease_list = []
    curing_drug_list = []
    side_effects_from_drug_list = []

    def print_function(print_value, disease_list, curing_drug_list, side_effects_from_drug_list):
        if print_value==0:
            disease_list = search_disease_from_symptom(symptom, disease_list)
            print(len(disease_list))
            printlist(disease_list)
        elif print_value==1:
            curing_drug_list = search_curing_drug_from_symtom(symptom, curing_drug_list)
            print(len(curing_drug_list))
            printlist(curing_drug_list)
        elif print_value==2:
            side_effects_from_drug_list = search_side_effects_drug_from_symptom(symptom, side_effects_from_drug_list)
            print(len(side_effects_from_drug_list))
            printlist(side_effects_from_drug_list)

    start = time.time()

    if print_value in [0, 1, 2]:
        print_function(print_value, disease_list, curing_drug_list, side_effects_from_drug_list)

    if print_value == 3:
        print_function(0, disease_list, curing_drug_list, side_effects_from_drug_list)
        print_function(1, disease_list, curing_drug_list, side_effects_from_drug_list)
        print_function(2, disease_list, curing_drug_list, side_effects_from_drug_list)

    end = time.time()

    print("#####")
    print()
    print(f"time : {end - start}")


if __name__ == '__main__':
    main()