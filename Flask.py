from Recup_donnée_capteur import getTemp ,getHumidity , getPressure
from Adresseip import adresseIP
from flask import Flask ,render_template
from datetime import datetime, timedelta
import socket
import os
from pprint import pprint
from Database import insertValue , selectValue,deleteValue , deleteTable , createTable , selectSpecificValue
from envoie_mail import sendEmail

import paho.mqtt.client as mqtt # import the client1
import time 

broker_address="192.168.43.206"
broker_port=1883
#broker_address="iot.eclipse.org"  # use external broker
client = mqtt.Client() # create new instance
client.connect(broker_address)#,broker_port) # connect to broker
client.subscribe("Test",qos=1)
client.publish(topic = "house/main-light")#publis

# MQTT Brokers https://projetsdiy.fr/mosquitto-broker-mqtt-raspberry-pi/ 


# plus tard : https://freeboard.io
# Plus tard : www.myconstellation.io
app= Flask(__name__)

# MQTT 

# Ip ubuntu : 172.17.251.30

# Ip Rasberry : 172.17.251.85 / 192.168.43.206


# mosquitto_sub -h localhost -v -t test_channel

# mosquitto_pub -h (address ip de ubuntu) -t test_channel -m "Hello Rasberry Pi"


@app.route("/gT/<rep>/<date>")
def graTemp (rep,date):
	d=datetime.now()
	allValue = []
	allTime = []
	if rep == "temp":
		valeur = selectSpecificValue('temperature',date)
	elif rep == "humi":
		valeur = selectSpecificValue('pressure',date)
	elif rep == "press":
		valeur = selectSpecificValue('humidite',date)
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
	# insertValue(str(getTemp()),str(getPressure()),str(getHumidity()))


	# -------------------- Supprimer les valeurs --------------------
	# deleteValue()

	# -------------------- Supprimer la table info --------------------
	# deleteTable()

	# -------------------- Creation de la table info --------------------
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