# -*- encoding: utf-8 -*-

from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug import generate_password_hash, check_password_hash
import requests
import json
import googlesheet
from os import environ, path

k = environ.get('OMDBK')

if not k:
    print('An OMDB API Key is required. export OMDBK="yourkey"')
    exit(1)

auth = HTTPBasicAuth()

users = {
        "user": generate_password_hash("password")  # TODO: changeme
}

app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to this amazing CaseStudy !"

def smaller(jsonstr):
    # filter movie txt for Poster, Title, Year, Director
    txt = json.loads(jsonstr)
    text = {}
    text['Poster'] = txt['Poster']
    text['Title'] =  txt['Title']
    text['Year']  =  txt['Year']
    text['Director'] = txt['Director']
    return json.dumps(text)

@app.route("/films")
def films():
    # could be Fast & Furious but need to understand how they handle & in title vs. search
    resp = requests.get('http://www.omdbapi.com/?s=' + "fast furious", params={'apikey':k})
    enrich = request.args.get('enrich', None)
    if enrich:
        res = []
        search = json.loads(resp.content)
        for f in search['Search']:
            print(f)
            resp = requests.get('http://www.omdbapi.com/?i=' + f['imdbID'], params={'apikey':k})
            res.append(smaller(resp.content))
        return str(res)
    else:
        return resp.content

@app.route("/pirates")
@auth.login_required
def pirates():
    resp = requests.get('http://www.omdbapi.com/?s=' + "pirates", params={'apikey':k})
    allres = []
    search = json.loads(resp.content)
    if 'Search' in search:
        for f in search['Search']:
            # format answers
            # keep only smaller (Poster, Title, Year, Director, before_2015, paulwalker in it?, common starwars
            rep = requests.get('http://www.omdbapi.com/?i=' + f['imdbID'], params={'apikey':k})
            small = json.loads(smaller(rep.content))
            res = json.loads(rep.content)
            small['before_2015'] = int(res['Year']) < 2015
            small['paulwaker'] = "Paul Walker" in res['Actors']
            stars = [ "Mark Hamill", "Harrison Ford", "Carrie Fisher"] # TODO: add more actors if necessary, maybe make it dynamic
            small["fast_wars_actors"] = str([a for a in list(set(stars).intersection(set(res['Actors'])))]) # str for googlesheet
            allres.append(small)
        if path.exists('token.json'):
            googlesheet.writeentry(list(small.values()))
        return str(allres)
    else:
        return resp.content

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

app.run(debug=True)
