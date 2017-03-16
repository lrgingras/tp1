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


import sqlite3


def build_dictionary_list(curseur):
    # Tous les curseurs sont tranférés dans une liste de disctionnaire.
    liste_article = []
    for row in curseur:
        dict_article = {}
        for i in range(0, len(row)):
            dict_article[curseur.description[i][0]] = row[i]
        liste_article.append(dict_article)
    return liste_article


class Database:
    def __init__(self):
        self.connection = None

    # Connection à la base de données
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/crm.db')
        return self.connection

    # Fermeture de la connexion de la base de données
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    # Requêtes pour la page d'acceuil
    def get_article_limite(self, limite):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, titre, identifiant, auteur, "
                       "       date_publication, paragraphe "
                       "from article "
                       "where date_publication <= date('now', 'localtime') "
                       "Order by date_publication Desc "
                       "limit ?", [limite])
        return build_dictionary_list(cursor)

    # Requête basé sur une recherche partiel sur les champs titre ou paragraphe
    def get_recherche_article(self, valeur_recherche):
        cursor = self.get_connection().cursor()
        cursor.execute("select titre, date_publication, identifiant "
                       "from article "
                       "where date_publication <= date('now','localtime') and "
                       "      (titre like ? or paragraphe like ?) "
                       "Order by date_publication Desc",
                       ("%"+valeur_recherche+"%", "%"+valeur_recherche+"%"))
        return build_dictionary_list(cursor)

    # Requête basé sur une recherche sur le champs identifiant
    def get_article_identifiant(self, identifiant):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, titre, identifiant, auteur, "
                       "       date_publication, paragraphe "
                       "from article "
                       "where date_publication <= date('now','localtime') and "
                       "      identifiant = ?",
                       [identifiant])
        dictionary = build_dictionary_list(cursor)
        if len(dictionary) == 0:
            return None
        else:
            return dictionary[0]

    # UTILISATION UNIQUEMENT POUR LES PAGES D'ADMINISTRATION
    # Requête qui retourne tous les enregistrements, incluant ceux ayant une
    # date de publication dans le future.
    def get_tous_articles_pour_page_admin(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select titre, date_publication, identifiant "
                       "from article order by titre")
        return build_dictionary_list(cursor)

    # UTILISATION UNIQUEMENT POUR LES PAGES D'ADMINISTRATION
    # Requête basé sur une recherche sur le champs identifiant
    # La date de publication n'est pas prise en considération puisque c'est
    # pour la section ADMINISTRATEUR
    def get_article_identifiant_admin(self, identifiant):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, titre, identifiant, auteur, "
                       "       date_publication, paragraphe "
                       "from article "
                       "where identifiant = ?",
                       [identifiant])
        if cursor.rowcount == 0:
            return None
        return build_dictionary_list(cursor)[0]

    # UTILISATION UNIQUEMENT POUR LES PAGES D'ADMINISTRATION
    # Requête de mise à jour des articles.
    def set_mise_a_jour_article_admin(self, titre, paragraphe, identifiant):
        cursor = self.get_connection().cursor()
        cursor.execute("select id  "
                       "from article "
                       "where identifiant = ?",
                       [identifiant])
        data = cursor.fetchone()
        if data is None:
            return 1
        else:
            cursor.execute("update article set titre = ?, paragraphe = ? "
                           "where identifiant = ?",
                           (titre, paragraphe, identifiant))
            self.get_connection().commit()
            return 0

    # UTILISATION UNIQUEMENT POUR LES PAGES D'ADMINISTRATION
    # Requête d'insertion des nouveaux articles.
    def set_nouvel_article_admin(self, titre, identifiant, auteur,
                                 date_publication, paragraphe):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("select id  "
                       "from article "
                       "where identifiant = ?",
                       [identifiant])
        data = cursor.fetchone()
        if data is None:
            cursor.execute("insert into article "
                           "   (titre, identifiant, auteur, date_publication, "
                           "    paragraphe) values(?, ?, ?, ?, ?)",
                           (titre, identifiant, auteur,
                            date_publication, paragraphe))
            connexion.commit()
            return 0
        else:
            return 1
