from flask import Flask,request, render_template
import re
import pandas as pd



#import ipywidgets as widgets
#from ipywidgets import interactive
#import numpy as np
#import os

app = Flask(__name__)

#PATH=os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def welcome():
    HtmlFile = open('./src/Activo/index.html', 'r', encoding='utf-8')
    saludo = HtmlFile.read()
    return saludo
"""
@app.route("/", methods=['POST', 'GET'])
def main():
    beers=pd.read_csv("/data/myuntapp.csv")
    if request.method=='POST':
        beer_name=request.form['beer_name']
        beer_type=request.form['beer_type']
        beer_abv=request.form['beer_abv']
        beer_ibu=request.form['beer_ibu']
        rating_score=request.form['rating_score']
        global_rating_score=request.form['global_rating_score']
        photo_url=request.form['photo_url']
"""
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

