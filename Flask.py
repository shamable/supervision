from Recup_donnée_capteur import getTemp ,getHumidity , getPressure
from Adresseip import adresseIP
from flask import Flask ,render_template
from datetime import datetime, timedelta
import socket
import os
from pprint import pprint
from Database import insertValue , selectValue,deleteValue , deleteTable , createTable , selectSpecificValue , selectAllValue
from envoie_mail import sendEmail
import json

import paho.mqtt.client as mqtt # install with pip3 install paho-mqtt
import time 

# plus tard : https://freeboard.io
# Plus tard : www.myconstellation.io

app= Flask(__name__)


def connect_mqtt(temp,humi,press):
	d=datetime.now()
	channel = "test_channel"

	data_send={"Temperature": temp ,"Humidity" : humi ,"Pressure" : press}
	client = mqtt.Client()

	client.loop_start()
	client.connect("192.168.1.27",1883,60)# Avoir l'adresse ip de l'autre machine 
	if client:
	#while True : 
		client.subscribe(channel)
		client.publish(channel,json.dumps(data_send),1)
		print("MQTT send : " +str(data_send))

	client.loop_stop()
	client.disconnect()
	return

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

	insertValue(str(getTemp()),str(getPressure()),str(getHumidity()))
	connect_mqtt(getTemp(),getHumidity(),getPressure())

	# -------------------- Supprimer les valeurs ---------------------

	# deleteValue()

	# -------------------- Supprimer la table info --------------------

	# deleteTable()

	# -------------------- Creation de la table info ------------------

	# createTable()

	tableau = selectValue(False)
	# ATTENTION LA BASE DE DONNÉES ET EN HEURE D'été
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