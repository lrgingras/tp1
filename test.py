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
def index():
    limite = "10"
    articles = get_db().get_article_limite(limite)
    if len(articles) == 0:
        return render_template('aucun_article.html')
    else:
        return render_template('liste.html', articles=articles)


@app.route('/liste')
def get_tous_articles():
    articles = get_db().get_tous_articles()
    if len(articles) == 0:
        return render_template('aucun_article.html')
    else:
        return render_template('liste.html', articles=articles)


@app.route('/recherche/<valeur_recherche>')
def get_recherche_article(valeur_recherche):
    articles = get_db().get_recherche_article(valeur_recherche)
    if len(articles) == 0:
        return render_template('aucun_article.html')
    else:
        return render_template('liste.html', articles=articles)


@app.route('/article/<identifiant>')
def get_article_identifiant(identifiant):
    articles = get_db().get_article_identifiant(identifiant)
    if len(articles) == 0:
        return render_template('404.html')
    else:
        return render_template('liste.html', articles=articles)


@app.route('/admin')
def get_article_admin():
    articles = get_db().get_tous_articles_pour_page_admin()
    return render_template('liste.html', articles=articles)


@app.route('/admin/<identifiant>')
def get_article_admin_identifiant(identifiant):
    articles = get_db().get_article_identifiant_admin(identifiant)
    if len(articles) == 0:
        return render_template('404.html')
    else:
        return render_template('liste.html', articles=articles)


@app.route('/set_mise_a_jour_article_admin/<identifiant>')
def set_mise_a_jour_article_admin(identifiant):
    paragraphe = 'paragraphe ' + identifiant + identifiant + identifiant
    titre = 'titre ' + identifiant + identifiant
    statut = get_db().set_mise_a_jour_article_admin(titre, paragraphe,
                                                    identifiant)
    if statut == 0:
        return get_article_admin()
    else:
        return render_template('erreur_de_mise_a_jour.html')


@app.route('/set_nouvel_article_admin/<identifiant>')
def set_nouvel_article_admin(identifiant):
    titre = "Le titre de " + identifiant
    auteur = "L'auteur de " + identifiant
    date_publication = '2017-01-31'
    paragraphe = "Le paragraphe de " + identifiant
    statut = get_db().set_nouvel_article_admin(titre, identifiant, auteur,
                                               date_publication, paragraphe)
    if statut == 0:
        return get_article_admin()
    else:
        return render_template('erreur_de_mise_a_jour.html')


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

if __name__ == '__main__':
    app.run(debug=True)
