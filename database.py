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

class Database:
    def __init__(self):
        self.connection = None

    #Connection à la base de données
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/crm.db')
        return self.connection

    #Fermeture de la connexion de la base de données
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()


    #Requêtes pour la page d'acceuil
    def get_article_limite(self, limite):
        cursor = self.get_connection().cursor()
        cursor.execute(("select id, titre, identifiant, auteur, "
                       "       date_publication, paragraphe "
                       "from article "
                       "where date_publication <= date('now', 'localtime') "
                       "Order by date_publication "
                       "limit ?"), (limite))
        return cursor.fetchall()

    #Requête basé sur une recherche partiel sur le champs titre ou paragraphe
    def get_recherche_article(self, valeur_recherche):
        cursor = self.get_connection().cursor()
        cursor.execute("select titre, date_publication from article "
                       "where titre like ? or paragraphe like ? "
                       "Order by date_publication",
                       ("%"+valeur_recherche+"%", "%"+valeur_recherche+"%"))
        return cursor.fetchall()

    #Requête basé sur une recherche sur le champs identifiant
    def get_article(self, identifiant):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, titre, identifiant, auteur, "
                       "       date_publication, paragraphe "
                       "from article "
                       "where identifiant = '?'",
                       identifiant)
        return cursor.fetchall()

    def get_tous_articles(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select titre, date_publication from article order by titre")
        return cursor.fetchall()
        
    def set_article(self, titre, paragraphe):
        cursor = self.get_connection().cursor()
        cursor.execute("update article set titre = ?, paragraphe = ? "
                       "where article = '?'", (titre, paragraphe))
        connection.commit()

    def set_nouvel_article(self, id_article, titre, identifiant, auteur,
                           date_publication, paragraphe):
        cursor = self.get_connection().cursor()
        cursor.execute("insert into article "
                       "   (id, titre, identifiant, auteur, date_publication, "
                       "    paragraphe) values(?, ?, ?, ?, ?)",
                       (id_article, titre, identifiant, auteur, date_publication, paragraphe))
        connection.commit()

    def get_albums_to_delete(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select titre from album")
        albums = cursor.fetchall()
        return [album[0] for album in albums]

    def insert_artist_to_delete(self, name):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into artiste(nom, est_solo, nombre_individus) "
                        "values(?, ?, ?)"), (name, 0, 0))
        connection.commit()
