from Recup_donnée_capteur import getTemp ,getHumidity , getPressure
from Adresseip import adresseIP
from flask import Flask ,render_template, request , redirect
from datetime import datetime, timedelta
import socket
import os
from pprint import pprint
from Database import insertValue , selectValue,deleteValue , deleteTable , createTable , selectSpecificValue , selectAllValue
from Database_gestion import SelectALlMail,CreateTableEmail,deleteTableEmail , SelectSeuilValue , CreateTableValue, deleteTableValue, InsertTableEmail,selectspecificMail
from envoie_mail import sendEmail
from mqtt import connect_mqtt

import time 

# plus tard : https://freeboard.io
# Plus tard : www.myconstellation.io

app= Flask(__name__)


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
		valeur = selectSpecificValue('pressure',date)
		rep = "Humidite"
		color = 'rgb(0,0,255)'
	elif rep == "pres":
		valeur = selectSpecificValue('humidite',date)
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

@app.route("/send",methods=['GET','POST'])
def send():
	if request.method == 'POST' :
		# Cree l'alerte si une adresse email exsite déja
		email = request.form['email']
		mdp = request.form['mdp']

		# CreateTableEmail()

		# deleteTableEmail()
		print("Email : "+email+"    Mdp : "+mdp)
		result = selectspecificMail(email)
		for row in result :
			if email == row[0] :
				# Dire a l'utilisateur que le mail exsite est déja utiliser
				return redirect("/register")
				

		InsertTableEmail(email,mdp)
		return redirect("/")
	return redirect("/register")

@app.route("/connect",methods=['GET','POST'])
def connect():
	if request.method == 'POST' :
		email = request.form['email']
		mdp = request.form['mdp']

		result = selectspecificMail(email)
		for row in result :
			if email == row[0] and mdp == row[1]:
				return redirect("/")
	# Faire en sorte que l'utilisateur sache que son MDP ou son email est faux 
	return redirect("/register")


@app.route("/")
def home():
	pressiontable = []
	humiditetable = []
	temperaturetable = []
	horairetable = []
	d= datetime.now()
	y = d.strftime('%Y-%m-%d')
	if getTemp() > 80:
		sendEmail('Temperature Trop haute','temperature','haute')
	elif getTemp() < 10 :

		sendEmail('Temperature Trop basse','temperature','basse')
	if getHumidity() > 80: 

		sendEmail('Humidité Trop haute','Humidité','haute')
	elif  getHumidity() < 5 :

		sendEmail('Humidité Trop basse','Humidité','basse')
	if getPressure() > 1114 :

		sendEmail('Pression Trop haute','Pression','haute')
	elif getPressure() < 400 :

		sendEmail('Pression Trop basse','Pression','basse')

	# -------------------- Insertion de valeur ----------------------

	# insertValue(str(getTemp()),str(getPressure()),str(getHumidity()))
	# connect_mqtt(getTemp(),getHumidity(),getPressure())

	# -------------------- Supprimer les valeurs ---------------------

	# deleteValue()

	# -------------------- Supprimer la table info --------------------

	# deleteTable()

	# -------------------- Creation de la table info ------------------

	# createTable()

	tableau = selectValue(False)
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
		timegraph = horairetable
		)

if __name__ =="__main__":
	app.run(debug=True,host=adresseIP(),port='5000')