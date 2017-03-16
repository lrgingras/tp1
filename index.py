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
from flask import make_response
from flask import g
from flask import redirect
from flask import request
import datetime
import re
from database import Database
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database

def validation(form, mode):
    titre = form['titre']
    paragraphe = form['paragraphe']
    identifiant = form['identifiant']
    valide = True
    dict_validation = {}
    if mode == 'insert':
        auteur = form['auteur']
        date_publication = form['date_publication']
        # Validation de l'Identifiant
        if len(identifiant) == 0:
            dict_validation['identifiant'] = "L'identifiant est obligatoire."
            valide = False
        elif len(identifiant) > 50:
            dict_validation['identifiant'] = u"L'identifiant doit être d'un maximum de 50 caractères."
            valide = False
        elif not re.match('[a-zA-Z_0-9]', identifiant):
            dict_validation['identifiant'] = u"L'identifiant ne doit utiliser que les caractères alphanumériques ainsi que le souligné(_)."
            valide = False
        else:
            dict_validation['identifiant'] = 'Valide'
        # Validation de l'Auteur
        if len(auteur) == 0:
            dict_validation['auteur'] = "L'auteur est obligatoire."
            valide = False
        elif len(auteur) > 100:
            dict_validation['auteur'] = u"L'auteur doit être d'un maximum de 100 caractères."
            valide = False
        else:
            dict_validation['auteur'] = 'Valide'
        # Validation de la Date de Publication
        if len(date_publication) == 10:
            dict_validation['date_publication'] = 'Valide'
            try:
                datetime.datetime.strptime(date_publication, '%Y-%m-%d')
            except ValueError:
                dict_validation['date_publication'] = "La date de publication n'est pas valide."
                valide = False

    # Validation du Titre
    if len(titre) == 0:
        dict_validation['titre'] = "Le titre est obligatoire."
        valide = False
    elif len(titre) > 100:
        dict_validation['titre'] = u"Le titre doit être d'un maximum de 100 caractères."
        valide = False
    else:
        dict_validation['titre'] = "Valide"
    # Validation du Paragraphe
    if len(paragraphe) == 0:
        dict_validation['paragraphe'] = "Le paragraphe est obligatoire."
        valide = False
    elif len(paragraphe) > 500:
        dict_validation['paragraphe'] = u"Le paragraphe doit être d'un maximum de 500 caractères."
        valide = False
    else:
        dict_validation['paragraphe'] = 'Valide'
    
    # Traitement selon validation
    if valide:
        if mode == 'insert':
            statut = get_db().set_nouvel_article_admin(titre, identifiant,
                                                       auteur,date_publication,
                                                       paragraphe)
        elif mode == 'update':
            statut = get_db().set_mise_a_jour_article_admin(titre, paragraphe,
                                                            identifiant)

        if statut == 0:
            return redirect('/admin')
        else:
            dict_validation['identifiant'] = u"Cet identifiant est déjà utilisé."
            return render_template('correctionArticle.html', titre="Erreur", sous_titre="svp corriger",
                                                 erreur=dict_validation, article=request.form)
    else:
        if mode == 'update':
            return render_template('editionArticle.html', titre="Erreur", sous_titre="svp corriger",
                                                 erreur=dict_validation, article=request.form)
        else:
            return render_template('correctionArticle.html', titre="Erreur", sous_titre="svp corriger",
                                                 erreur=dict_validation, article=request.form)
        return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', titre="404",
                           sous_titre="Cette page est introuvable."), 404

@app.route('/')
def page_accueil():
    limite='5'
    articles = get_db().get_article_limite(limite)
    return render_template('index.html', titre="Acceuil",
                           sous_titre=u"Pour les amoureux de la simplicité",
                           articles=articles)

@app.route('/article/<identifiant>')
def get_article_identifiant(identifiant):
    article = get_db().get_article_identifiant(identifiant)
    if article == None:
        return redirect('/erreur')
    else:
        return render_template('liste.html', titre=article['titre'],
                           sous_titre=article['auteur'] + ' (' + article['date_publication'] + ')', article=article)

@app.route('/edition/<identifiant>')
def get_article_edition(identifiant):
    article = get_db().get_article_identifiant_admin(identifiant)
    if article == None:
        return redirect('/erreur')
    else:
        return render_template('editionArticle.html', titre=u'Édition',
                           sous_titre=article['titre'], article=article)

@app.route('/recherche')
def get_recherche_article():
    valeur_recherche = request.args.get('valeur_recherche','')
    articles = get_db().get_recherche_article(valeur_recherche)
    if len(articles) == 0:
        return render_template('aucun_article.html', titre="Aucun article",
                           sous_titre= u"Aucun article ne contient le mot clef : {0}".format(valeur_recherche))
    else:
        if len(articles) == 1:
            sous_titre = u"1 article contient votre mot clef : {0}".format(valeur_recherche)
        else:
            sous_titre = u"{0} articles contiennent votre mot clef : {1}".format(len(articles), valeur_recherche)
        return render_template('rechercheArticles.html',titre="Recherche", sous_titre=sous_titre, valeur_recherche=valeur_recherche, articles=articles)
        
        
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()

@app.route('/admin')
def page_admin():
    articles = get_db().get_tous_articles_pour_page_admin()
    return render_template('admin.html', titre="Administration",
                           sous_titre=u"Gérez votre site directement de cette page",
                           articles=articles)

@app.route('/admin-nouveau')
def show_form():
    return render_template('article.html', titre="Nouvel article")

@app.route('/ajout-article', methods=['POST'])
def page_ajout():
    mode = "insert"
    return validation(request.form, mode)

@app.route('/edition-article', methods=['POST'])
def page_edition():
    article = get_db().get_article_identifiant_admin(request.form['identifiant'])
    article['titre'] = request.form['titre']
    article['paragraphe'] = request.form['paragraphe']
    mode = "update"
    return validation(article, mode)

if __name__ == '__main__':
    app.run(debug=True)
       