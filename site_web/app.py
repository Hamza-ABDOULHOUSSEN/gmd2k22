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
    DrugbankFormQuery = forms.DrugbankFormQuery(request.form)
    arguments = request.args

    query = "none"
    content = []
    count = 0

    if len(arguments) != 0:
        query = arguments["query"]
        content = drugbank_query(query)
        count = len(content)

    return render_template("test.html", DrugbankFormQuery=DrugbankFormQuery, query=query, count=count, content=content)






if __name__ == '__main__':
    app.run()
    query = "\"id : DB0000*\""
    content = drugbank_query(query)
    print(str(content))
