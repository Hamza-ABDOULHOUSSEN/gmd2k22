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

