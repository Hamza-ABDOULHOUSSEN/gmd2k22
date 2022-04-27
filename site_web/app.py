from flask import Flask, request, render_template

from requests import *
import forms

app = Flask(__name__)

disease_list, curing_drug_list, side_effects_from_drug_list = [], [], []
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

@app.route('/test', methods = ["GET"])
def test():
    FormQuery = forms.FormQuery(request.form)
    arguments = request.args

    query = "none"
    count_disease_list, count_curing_drug_list, count_side_effects_from_drug_list = 0, 0, 0

    global disease_list, curing_drug_list, side_effects_from_drug_list
    global content_sider_id

    if len(arguments) != 0:
        query = arguments["query"]
        symptom = query.lower()

        disease_list, curing_drug_list, side_effects_from_drug_list = [], [], []
        content_sider_id = []

        disease_list = search_disease_from_symptom(symptom, disease_list)
        curing_drug_list = search_curing_drug_from_symtom(symptom, curing_drug_list)

        content_sider_id = get_sider_id(symptom)
        content_id_start = 0

        M = min(content_id_start+5, len(content_sider_id))
        content_id_start+=5

        side_effects_from_drug_list = search_side_effects_drug_from_content_sider_id(content_sider_id[content_id_start:content_id_start+M], side_effects_from_drug_list)

        count_disease_list, count_curing_drug_list, count_side_effects_from_drug_list = len(disease_list), len(curing_drug_list), len(side_effects_from_drug_list)

    return render_template("test.html", FormQuery=FormQuery, query=query,
                           count_disease_list = count_disease_list,
                           count_curing_drug_list = count_curing_drug_list,
                           count_side_effects_from_drug_list = count_side_effects_from_drug_list,
                           disease_list = disease_list,
                           curing_drug_list = curing_drug_list,
                           side_effects_from_drug_list = side_effects_from_drug_list
                           )

@app.route('/test', methods = ["GET"])
def plus():
    global content_id_start
    global disease_list, curing_drug_list, side_effects_from_drug_list
    global content_sider_id

    M = min(content_id_start + 5, len(content_sider_id))
    content_id_start += 5

    side_effects_from_drug_list += search_side_effects_drug_from_content_sider_id(content_sider_id[content_id_start:content_id_start + M], side_effects_from_drug_list)

    count_disease_list, count_curing_drug_list, count_side_effects_from_drug_list = len(disease_list), len(curing_drug_list), len(side_effects_from_drug_list)

    return render_template("test.html",
                           count_disease_list=count_disease_list,
                           count_curing_drug_list=count_curing_drug_list,
                           count_side_effects_from_drug_list=count_side_effects_from_drug_list,
                           disease_list=disease_list,
                           curing_drug_list=curing_drug_list,
                           side_effects_from_drug_list=side_effects_from_drug_list
                           )

if __name__ == '__main__':
    app.run()
    query = "\"id : DB0000*\""
    content = drugbank_query(query)
    print(str(content))
