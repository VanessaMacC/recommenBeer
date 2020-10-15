from flask import Flask,request,render_template
import re
import pandas as pd

import ipywidgets as widgets
from ipywidgets import interactive
import numpy as np
import os

app = Flask(__name__)

#PATH=os.path.dirname(os.path.abspath(__file__))

beers = pd.read_csv("./data/myuntapp.csv", engine = 'python')
beers = beers[['beer_name', 'brewery_name', 'beer_type', 'beer_abv', 'beer_ibu', 
               'venue_name', 'venue_city', 'venue_state', 'venue_country',
               'venue_lat', 'venue_lng', 'rating_score', 'created_at', 'checkin_url',
               'beer_url', 'brewery_url', 'brewery_country', 'brewery_city',
               'brewery_state', 'flavor_profiles', 'purchase_venue', 'serving_type',
               'checkin_id', 'bid', 'brewery_id', 'photo_url', 'global_rating_score',
               'global_weighted_rating_score']]

beers = beers.fillna(0)

df=beers.copy()

df=df[['beer_name','beer_type','beer_abv','beer_ibu','rating_score','global_rating_score','photo_url']]

ratings = df.pivot_table(values='rating_score', index='beer_type', columns='beer_name')
ratings.fillna(0, inplace=True)
beer_index = ratings.columns
list(ratings.columns)

corr_matrix= np.corrcoef(ratings.T)
corr_matrix.shape

def get_beer_similarity(beer_name):  
    '''Returns correlation vector for a beer'''
    beer_idx = list(beer_index).index(beer_name)
    return corr_matrix[beer_idx]

a=get_beer_similarity("Jamonera")
a.shape

def get_beer_recommendations(stl):  
    '''given a set of beers, it returns all the beers sorted by their correlation with the style'''
   
    beer_similarities = np.zeros(corr_matrix.shape[0])
    for Id in stl:
        beer_similarities = beer_similarities + get_beer_similarity(Id)
    similarities_df = pd.DataFrame({
        'beer_name': beer_index,
        'sum_similarity': beer_similarities
        })
    similarities_df = similarities_df[~(similarities_df.beer_name.isin(stl))]
    similarities_df = similarities_df.sort_values(by=['sum_similarity'], ascending=False)
    return similarities_df.beer_name.head(6)

sample_style = 'IPA - American'
df[df.beer_type==sample_style].sort_values(by=['rating_score'], ascending=False)

sample_style_beers = df[df.beer_type==sample_style].beer_name.tolist()  
recommendations = get_beer_recommendations(sample_style_beers)

df1=df[df.beer_type==sample_style].head(6)
df1=df1.filter(items=['beer_type'])
df1.reset_index(inplace=True)

df_final=recommendations.to_frame()
df_final.reset_index(inplace=True)

df_final_test=pd.concat([df1['beer_type'], df_final['beer_name']], axis=1)

df_filtered = df[df['beer_type'] == "IPA - American"]
df_filtered.head(10)

items = sorted(df['beer_type'].unique().tolist())

def view(x=''):
    if x==x: return(get_beer_recommendations(df[df.beer_type==x].beer_name.tolist()))
     
    
w = widgets.Select(options=items)
interactive(view, x=w)

def get_top_beers (a):
    favoured_beer_index = list(beer_index).index(a)
    P = corr_matrix[favoured_beer_index]
#sólo devolvemos las cervezas con la mayor correlación con el nombre de la cerveza dada
    return(list(beer_index[(P>0.5) & (P<1.0)][:5]))

get_top_beers('Fyr & Flamme')

items2 = sorted(df['beer_name'].unique().tolist())

def view(x=''):
    if x==x: return(get_top_beers(x))
       
w = widgets.Select(options=items2)
interactive(view, x=w)


@app.route('/')
def welcome():
    HtmlFile = open('./src/Activo/index.html', 'r', encoding='utf-8')
    saludo = HtmlFile.read()
    return saludo


"""
@app.route("/beer", methods=['POST', 'GET'])
def main():
    beers=beers
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

