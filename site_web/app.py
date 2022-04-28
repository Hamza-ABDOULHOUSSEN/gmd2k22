from flask import Flask, request, render_template

from requests import *
from concat_dict import *
import forms

app = Flask(__name__)

disease_list, curing_drug_list, side_effects_from_drug_list = {}, {}, {}
side_effects_from_drug_list_drugbank = {}
content_sider_id = []
content_id_start = 0

@app.route('/', methods = ["GET"])
def index():
    return render_template("index.html")

@app.route('/ex_drugbank_query', methods = ["GET"])
def ex_drugbank_query():
    DrugbankFormQuery = forms.DrugbankFormQuery(request.form)
    arguments = request.args

    query = "none"
    content = []
    count = 0

    if len(arguments) != 0:
        query = arguments["query"]
        content = drugbank_query(query)
        count = len(content)

    return render_template("ex_drugbank_query.html", DrugbankFormQuery=DrugbankFormQuery, query=query, count=count, content=content)

@app.route('/myPage', methods = ["GET"])
def myPage():
    DrugbankFormQuery = forms.DrugbankFormQuery(request.form)
    arguments = request.args

    query = "none"
    content = []
    count = 0

    if len(arguments) != 0:
        query = arguments["query"]
        content = drugbank_query(query)
        count = len(content)

    return render_template("myPage.html", DrugbankFormQuery=DrugbankFormQuery, query=query, count=count, content=content)

@app.route('/requete', methods = ["GET"])
def requete():
    #query = "SELECT *"
    query = "\"id : DB0000*\""
    content = drugbank_query(query)
    return render_template("requete.html", content=content)

@app.route('/test', methods = ["GET", "POST"])
def test():
    FormQuery = forms.FormQuery(request.form)
    arguments = request.args

    query = "none"
    count_disease_list, count_curing_drug_list, count_side_effects_from_drug_list = 0, 0, 0

    global content_id_start
    global disease_list, curing_drug_list, side_effects_from_drug_list
    global side_effects_from_drug_list_drugbank
    global content_sider_id

    if request.method == 'POST':
        query = "pas none"
        M = min(content_id_start + 5, len(content_sider_id))
        content_id_start += 5

        side_effects_from_drug_list = search_side_effects_drug_from_content_sider_id(content_sider_id[content_id_start:content_id_start + M], side_effects_from_drug_list)

        count_disease_list, count_curing_drug_list, count_side_effects_from_drug_list = len(disease_list), len(curing_drug_list), len(side_effects_from_drug_list)

        return render_template("test.html", FormQuery=FormQuery, query=query,
                               count_disease_list=count_disease_list,
                               count_curing_drug_list=count_curing_drug_list,
                               count_side_effects_from_drug_list=count_side_effects_from_drug_list,
                               disease_list=disease_list,
                               curing_drug_list=curing_drug_list,
                               side_effects_from_drug_list=side_effects_from_drug_list
                               )

    else:
        if len(arguments) != 0:
            query = arguments["query"]

            disease_list, curing_drug_list, side_effects_from_drug_list = {}, {}, {}
            side_effects_from_drug_list_drugbank = {}
            content_sider_id = []

            # SEARCH FOR OR
            symptoms = query.split(" OR ")

            for symptom in symptoms:

                # SEARCH FOR AND
                and_parse_symptoms = symptom.split(" AND ")

                disease_list_and, curing_drug_list_and = {}, {}
                side_effects_from_drug_list_drugbank_and = {}

                # initiate with first element
                symp = and_parse_symptoms[0].lower()
                disease_list_and = search_disease_from_symptom(symp, disease_list_and)
                curing_drug_list_and = search_curing_drug_from_symtom(symp, curing_drug_list_and)
                side_effects_from_drug_list_drugbank_and = search_side_effects_drug_from_drugbank(symp, side_effects_from_drug_list_drugbank_and)
                content_sider_id_and = get_sider_id(symp)

                and_parse_symptoms = and_parse_symptoms[1:]

                for symp in and_parse_symptoms:

                    symp = symp.lower()

                    # search from empty dict
                    disease_list_new = search_disease_from_symptom(symp, {})
                    curing_drug_list_new = search_curing_drug_from_symtom(symp, {})
                    side_effects_from_drug_list_drugbank_new = search_side_effects_drug_from_drugbank(symp, {})
                    content_sider_id_new = get_sider_id(symp)

                    # concatenation
                    disease_list_and = concat_dict_AND(disease_list_and, disease_list_new)
                    curing_drug_list_and = concat_dict_AND(curing_drug_list_and, curing_drug_list_new)
                    side_effects_from_drug_list_drugbank_and = concat_dict_AND(side_effects_from_drug_list_drugbank_and, side_effects_from_drug_list_drugbank_new)
                    content_sider_id_and = [value for value in content_sider_id_and if value in content_sider_id_new]

                # concatenate with global dict

                disease_list = concat_dict_OR(disease_list, disease_list_and)
                curing_drug_list = concat_dict_OR(curing_drug_list, curing_drug_list_and)
                side_effects_from_drug_list_drugbank = concat_dict_OR(side_effects_from_drug_list_drugbank, side_effects_from_drug_list_drugbank_and)
                content_sider_id = list(set(content_sider_id + content_sider_id_and))

            # search for side effects with all id
            content_id_start = 0
            M = min(content_id_start+5, len(content_sider_id))
            content_id_start+=5

            side_effects_from_drug_list = search_side_effects_drug_from_content_sider_id(content_sider_id[content_id_start:content_id_start+M], side_effects_from_drug_list)

            # CONCATENATE WITH DRUGS ON DRUGBANK
            side_effects_from_drug_list = concat_dict_OR(side_effects_from_drug_list, side_effects_from_drug_list_drugbank)

            count_disease_list, count_curing_drug_list, count_side_effects_from_drug_list = len(disease_list), len(curing_drug_list), len(side_effects_from_drug_list)

        return render_template("test.html", FormQuery=FormQuery, query=query,
                               count_disease_list = count_disease_list,
                               count_curing_drug_list = count_curing_drug_list,
                               count_side_effects_from_drug_list = count_side_effects_from_drug_list,
                               disease_list = disease_list,
                               curing_drug_list = curing_drug_list,
                               side_effects_from_drug_list = side_effects_from_drug_list
                               )


if __name__ == '__main__':
    app.run(debug=True)
