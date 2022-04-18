from flask import Flask, request, render_template
from requests import *
import forms


app = Flask(__name__)

@app.route('/', methods = ["GET"])
def index():
    return render_template("index.html")

