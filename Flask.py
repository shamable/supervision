from Recup_donnée_capteur import getTemp ,getHumidity , getPressure
from Adresseip import adresseIP
from flask import Flask, flash ,render_template, request , redirect , session
from datetime import datetime, timedelta
import socket
import os
from pprint import pprint
from Database import insertValue , selectValue,deleteValue , deleteTable , createTable , selectSpecificValue , selectAllValue

# Table adresse mail requete
from Database_gestion import SelectALlMail,CreateTableEmail,deleteTableEmail , InsertTableEmail, selectspecificMail, deleteOneEmail

# Table valeur seuil requete
from Database_gestion import  SelectSeuilValue , CreateTableValue, deleteTableValue,insertTableValue ,updateTableValue

# Table localisation requete
from Database_gestion import updateTableLocalisation, insertTableLocalsation, createTableLocalisation , SelectLocalisation
from envoie_mail import sendEmail

import time 

# Rajouter le code qui permet de lance le programme python de datainsert.py

# plus tard : https://freeboard.io
# Plus tard : www.myconstellation.io

app= Flask(__name__)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 
# Modification de la façon d'inserez les valeurs dans la base de données(BDD)
# 
# Elle ne se fait plus quand quelqung va sur la route("/")
#
# Maintenant il faut lancer le fichier datainsert.py dans le dossier supervision 
# Il enregistrera les valeurs toutes les 5min dans la BDD 
# Pour cela Ouvrir un terminal faire  cd Document/supervision
# Puis python3 datainsert.py
#
# Apres avoir lancée le fichier datainsert.py vous pouvez lancer votre serveur sur un autre terminal
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@app.route("/histo")
def histo():
	pressiontable = []
	humiditetable = []
	temperaturetable = []
	horairetable = []
	tableau = selectAllValue(False)
	titre = "Historique des temperature"
	for row in tableau:
		pressiontable.append(row[1]/10)
		humiditetable.append(row[2])
		temperaturetable.append(row[3])
		horairetable.append(row[4])
	return render_template(
		'histo.html',
		titre = titre,
		value = tableau,
		pressiongraph = pressiontable,
		humiditegraph = humiditetable,
		temperaturegraph = temperaturetable,
		timegraph = horairetable
	)

@app.route("/modifseuil",methods=['POST'])
def modifseuil():
	mintemp = request.form['1']
	maxtemp = request.form['2']
	minpres = request.form['3']
	maxpres = request.form['4']
	minhumi = request.form['5']
	maxhumi = request.form['6']
	updateTableValue(mintemp,'1')
	updateTableValue(maxtemp,'2')
	updateTableValue(minpres,'3')
	updateTableValue(maxpres,'4')
	updateTableValue(minhumi,'5')
	updateTableValue(maxhumi,'6')
	return redirect("/formSeuil",code = 302)


@app.route("/deleteEmail/<idmail>")
def deleteEmail(idmail):
	deleteOneEmail(idmail)
	return redirect("/mail")

@app.route("/mailtest",methods=['POST'])
def mailtest():
	sendEmail('Test','Test','Test')
	return redirect("/mail")


@app.route("/gT/<rep>/<date>")
def graTemp (rep,date):
	d=datetime.now()
	allValue = []
	allTime = []
	if rep == "temp":
		valeur = selectSpecificValue('temperature',date)
		rep = "Temperature"
		color = 'rgb(255,0,0)'
	elif rep == "hum":
		valeur = selectSpecificValue('humidite',date)
		rep = "Humidite"
		color = 'rgb(0,0,255)'
	elif rep == "pres":
		valeur = selectSpecificValue('pressure',date)
		rep = "Pression"
		color = 'rgb(0, 255,0)'
	annee=str(d)[:4]
	titre =" Temperature actuelle : "+ str(getTemp())+ " °C"
	for row in valeur:
		allValue.append(row[0])
		allTime.append(row[1])
	ndate = d + timedelta(days=1)
	pdate = d - timedelta(days=1) 
	return render_template(
		'graphTemp.html',
		d = d.strftime("%d-%m-%Y"),
		color = color,
		rep = rep,
		titre = titre,
		temp = getTemp(),
		value = allValue,
		time = allTime,
		prevDate = ndate.strftime("%Y-%m-%d"),
		nextDate = pdate.strftime("%Y-%m-%d")
	)

@app.route("/register")
def register():
	titre = "Enregistrez-vous"
	return render_template('register.html',
		title = titre)

@app.route("/send",methods=['POST'])
def send():
	if request.method == 'POST' :
		# Cree l'alerte si une adresse email exsite déja
		email = request.form['email']
		mdp = request.form['mdp']
		role = request.form['role']
		# CreateTableEmail()

		#deleteTableEmail()
		result = selectspecificMail(email)
		for row in result :
			if email == row[0] :
				flash("Cette email existe déja")
				return redirect("/register")
				

		InsertTableEmail(email,mdp ,role)
		flash('Connectez-Vous')
	return redirect("/register")

@app.route("/disconnect",methods=['GET','POST'])
def disconnect():
	session.clear()
	return redirect("/redirection")

@app.route("/redirection")
def redirection():
	return redirect("/")

@app.route("/formSeuil")
def formSeuil():
	temperature = []
	humidite = []
	pression = []
	titre = "Valeur de Seuil"
	valeur = SelectSeuilValue()
	for row in valeur:
		if row[3] == 'temperature':
			temperature.append(row[1])
		elif row[3] == 'humidite':
			humidite.append(row[1])
		elif row[3] == 'pression':
			pression.append(row[1])
	return render_template("formSeuil.html",
	title = titre,
	value = valeur)


@app.route("/formLocal")
def formLocal():
	titre = "Adressse du local"
	valeur = SelectLocalisation()
	return render_template("formLocal.html",
	title = titre,
	valeur = row)

@app.route("/modifLocal",methods=['POST'])
def modifLocal():
	nom = request.form['name']
	num = request.form['num']
	adresse = request.form['adresse']
	updateTableLocalisation(adresse,str(num),nom,'1')
	return redirect("/formLocal")

@app.route("/connect",methods=['POST'])
def connect():
	if request.method == 'POST' :
		email = request.form['email']
		mdp = request.form['mdp']

		result = selectspecificMail(email)
		for row in result :
			if email == row[0] and mdp == row[1]:
				session['logged_in'] = True
				if row[2] == 'A':
					session ['admin']= True
				return redirect("/")
			else : 
				error='Email ou mot de passe Incorect'
	# Faire en sorte que l'utilisateur sache que son MDP ou son email est faux 
	return redirect("/register")

@app.route("/mail")
def mail():
	titre = 'Email'
	res = SelectALlMail()
	return render_template("mail.html",
		title = titre,
		mail = res)


@app.route("/")
def home():
	valmin = 0
	valminpress = 0
	valminhumi = 0
	pressiontable = []
	humiditetable = []
	temperaturetable = []
	horairetable = []
	d= datetime.now()
	y = d.strftime('%Y-%m-%d')
	tableau = selectValue(False)
	localisation = SelectLocalisation()
	for row in localisation:
		name = row[3]
	# ATTENTION LAVEC L'HORAIRE DE LA BDD h-2(en été) h-1(hiver)  
	for row in tableau:
		pressiontable.append(row[1]/10)
		humiditetable.append(row[2])
		temperaturetable.append(row[3])
		horairetable.append(row[4])
	return render_template(
		"home.html",
		title = "Supervision salle serveur",
		temp = getTemp(),
		humi = getHumidity(),
		press = getPressure(),
		value = tableau,
		date = y,
		pressiongraph = pressiontable,
		humiditegraph = humiditetable,
		temperaturegraph = temperaturetable,
		timegraph = horairetable,
		session = session,
		name = name
		)

if __name__ =="__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True,host=adresseIP(),port='5000')