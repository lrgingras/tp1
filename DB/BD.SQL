create table article (
  id integer primary key,
  titre varchar(100),
  identifiant varchar(50),
  auteur varchar(100),
  date_publication text,
  paragraphe varchar(500)
);

insert into article (id, titre, identifiant, auteur, date_publication, paragraphe) values (1, 'Le titre', 'l identifiant', 'l auteur', '2017-12-31', 'Le paragraphe');