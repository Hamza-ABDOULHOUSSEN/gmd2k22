from flask import Flask, request, render_template

from requests import *
import forms

app = Flask(__name__)

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
    disease_list, curing_drug_list, side_effects_from_drug_list = [], [], []
    count_disease_list, count_curing_drug_list, count_side_effects_from_drug_list = 0, 0, 0

    if len(arguments) != 0:
        query = arguments["query"]
        disease_list, curing_drug_list, side_effects_from_drug_list = sb(query)
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
    app.run()
    query = "\"id : DB0000*\""
    content = drugbank_query(query)
    print(str(content))
