# Runme

	export ODBK="yourapikey"
	python brandcollcasestudy.py

# Usage

	# Visit http://hostname:5000
	curl http://localhost:5000/films
	curl 'http://localhost:5000/films?enrich=true'
	curl 'http://localhost:5000/films?enrich=true'
	curl 'http://user:password@localhost:5000/pirates' # behavior depends upon validity of token.json

# Setup

	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	python googlesheet.py # config auth and create token file see https://developers.google.com/sheets/api/quickstart/python (OPTIONAL)
	# set the id of google sheet to use, hardcode it in googlesheet.py (OPTIONAL)
	# set the password for basic auth, hardcode it in brandcollcasestudy.py (OPTIONAL)

# README

Ce projet répond à un énoncé pour démontrer quelques bases en construction d'application web.
Ce projet est écrit en *python* et utilise les librairies *flask* et *requests*.
De multiples options sont possibles pour l'hébergement:
	- AWS Lambda
	- https://www.pythonanywhere.com/
	- un container dans un environnement public (DockerFile, Manifest...)
	- une VM dans un cloud public (gunicorn ?)
	- un raspberry pi

Si jamais il y a beaucoup de traffic il faudrait cacher les requêtes, puis mettre en place du CDN et éventuellement scaler, c'est à dire configurer un ALB sur AWS ou augmenter le nombre d'instances définies et leur taille unitaire si le budget le permet.
La grosse faiblesse est ici le nombre de requêtes gratuites sur le site partenaire (1000)

# Authentication

	/pirates est une page protégée par Basic Auth

Utilisateurs configurable en dur dans brandcollcasestudy.py

# GSheet

Pour l'instant l'application est en test, pour utiliser la fonctionalité il faut communiquer votre email pour être ajouté à la liste des testeurs.
Les authorisations google sont contraignantes il y a un bel effort pour rendre l'application complètement disponible.
Il faut configurer le spreadsheet à utiliser dans le code. Par defaut cette partie n'est pas executée.
Une fois le fichier token.json existant le code qui écrit dans le sheet sera éxecuté, pour créer le token éxecutez :

	python googlesheet.py

# Next steps

	Ajouter une page web pour configurer les secrets
	Ajouter du front
	Packager l'appli pour obtenir un .oci deployable
	Ajouter une conf de déploiement continu
	Ajouter une conf de haute disponibilitée adaptée à la charge et au budget

# Rappel de l'énoncé:

	Backend OMDB avec (NodeJS + Typescript) ou Python :

	- Créer un projet capable de recevoir/répondre à des requêtes web, 
	- Faire des appels à l'API http://www.omdbapi.com/ et récupérer un listing des films (Image, Titre, Année, Réalisateur).
	- Mettre à disposition la liste des films "Fast & Furious" au format JSON dans notre serveur web via l'url /films
	- Créer une URL qui va récupérer la liste des films "Pirates des caraïbes" et qui va les stocker dans un Google Spreadsheet en ligne
	- Ajouter dans le Spreadsheet et dans le retour de l'API, les propriétés suivantes:
	-     Un propriété de type boolean pour indiquer si le film a été produit avant 2015
	-     Un propriété de type boolean pour indiquer si Paul Walker est un des acteurs du film
	-     Un propriété qui liste les acteurs en commun avec les films Star-Wars
	- Ajouter une sécurité simple permettant d'éviter les accès Anonymes à cette API
	- Expliquer en quelques phrases (README):
	-       Comment il est construit ?
	-       Comment faire fonctionner le projet ?
	-       Comment tu envisages la partie hébergement ?
	-       Comment tu vois une éventuelle montée en charge du système ?
	-       Ses forces, faiblesses, NEXT STEPS pour la mise en prod.
