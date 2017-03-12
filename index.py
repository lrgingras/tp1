# coding: utf8

# Copyright 2017 Louis-René Gingras/Alexandre Lemay-Lesny
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from database import Database
app = Flask(__name__)

@app.route('/')
def page_accueil():
    limite='5'
    articles = get_db().get_article_limite(limite)
    return render_template('index.html', titre="Acceuil",  sous_titre="Pour les amoureux de la simplicité",articles=articles)


@app.route('/article')
def page_prog_web_avancee():
    return render_template('about.html',titre="admin",sous_titre="")
    
@app.route('/recherche')
def recherche():
    valeur_recherche = 'es'
    articles = get_db().get_recherche_article(valeur_recherche) 
    return render_template('liste.html', articles=articles)
    
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/deux-listes')
def show_two_lists():
    artists = get_db().get_artists()
    albums = get_db().get_albums()
    return render_template('2listes.html', artists=artists, albums=albums)


@app.route('/vide')
def show_two_empty_lists():
    artists = []
    albums = []
    return render_template('2listes-vides.html', artists=artists, albums=albums)


@app.route('/formulaire')
def show_form():
    return render_template('form.html')


@app.route('/new', methods=['POST'])
def post_form():
    name = request.form['nom']
    if len(name) == 0:
        return render_template('form.html', erreur='Le nom est obligatoire')
    else:
        get_db().insert_artist(name)
        return redirect('/liste')
        

if __name__ == '__main__':
    app.run(debug=True)
       