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
from flask import redirect
from flask import request
import re
from database import Database
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', titre="404",
                           sous_titre="Cette page est introuvable."), 404

@app.route('/')
def page_accueil():
    limite='5'
    articles = get_db().get_article_limite(limite)
    return render_template('index.html', titre="Acceuil",
                           sous_titre="Pour les amoureux du simple et efficace",
                           articles=articles)

@app.route('/article/<identifiant>')
def get_article_identifiant(identifiant):
    articles = get_db().get_article_identifiant(identifiant)
    if len(articles) == 0:
        return render_template('404.html')
    else:
        return render_template('liste.html', articles=articles)

@app.route('/recherche')
def get_recherche_article():
   valeur_recherche = request.args.get('valeur_recherche','')
   articles = get_db().get_recherche_article(valeur_recherche)
   if len(articles) == 0:
        return render_template('aucun_article.html', titre="Aucun article",
                           sous_titre="Aucun article ne correspond avec la recherche.")
   else:
        sous_titre = "{0} articles contiennent votre mot clef : {1}".format(len(articles), valeur_recherche)
        return render_template('rechercheArticles.html',titre="Recherche", sous_titre=sous_titre, valeur_recherche=valeur_recherche, articles=articles)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()

@app.route('/admin-nouveau')
def show_form():
    return render_template('nouvelArticle.html',titre="Nouvel article")


@app.route('/ajout-article', methods=['POST'])
def post_form():
    titre = request.form['titre']
    identifiant = request.form['identifiant']
    auteur = request.form['auteur']
    date_publication = request.form['date_publication']
    paragraphe = request.form['paragraphe']
    valide = true
    dict_validation = {}
    # Validation du Titre
    if len(titre) == 0:
        dict_validation['titre'] = "Le titre est obligatoire."
        valide = false
    elif len(titre) > 100:
        dict_validation['titre'] = "Le titre doit être d'un maximum de 100 caractère."
        valide = false
    else:
        dict_validation['titre'] = "Valide"
    # Validation de l'Identifiant
    if len(identifiant) == 0:
        dict_validation['identifiant'] = "L'identifiant est obligatoire."
        valide = false
    elif len(identifiant) >= 50:
        dict_validation['identifiant'] = "L'identifiant doit être d'un maximum de 50 caractère."
        valide = false
    elif re.match('[a-zA-Z_0-9]', identifiant):
        dict_validation['identifiant'] = "L'identifiant ne doit utiliser que les caractères alphanumériques ainsi que le souligné(_)."
        valide = false
    else:
        dict_validation['identifiant'] = 'Valide'
    # Validation de l'Auteur
    if len(auteur) == 0:
        dict_validation['auteur'] = "L'auteur est obligatoire."
        valide = false
    elif len(auteur) > 100:
        dict_validation['auteur'] = "L'auteur doit être d'un maximum de 100 caractère."
        valide = false
    else:
        dict_validation['auteur'] = 'Valide'
    # Validation du Paragraphe
    if len(paragraphe) == 0:
        dict_validation['paragraphe'] = "Le paragraphe est obligatoire."
        valide = false
    elif len(paragraphe) > 500:
        dict_validation['paragraphe'] = "Le paragraphe doit être d'un maximum de 500 caractère."
        valide = false
    else:
        dict_validation['paragraphe'] = 'Valide'
    # Validation de la Date de Publication
    if len(date_publication) == 10:
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            dict_validation['date_publication'] = "La date de publication n'est pas valide."
            valide = false
    # Traitement selon validation
    if valide:
        statut = get_db().set_nouvel_article_admin(titre, identifiant, auteur,
                                                  date_publication, paragraphe)
        if statut == 0:
            return redirect('/admin')
        else:
            return render_template('erreur_de_mise_a_jour.html')
    else:
        response = make_response(render_template('admin-nouveau.html', 
                                                 erreur=dict_validation))
        response.set_cookie("nom", nom)
        response.set_cookie("prenom", prenom)
        response.set_cookie("identifiant", identifiant)
        response.set_cookie("date_validation", date_validation)
        response.set_cookie("paragraphe", paragraphe)
        return response

if __name__ == '__main__':
    app.run(debug=True)
       