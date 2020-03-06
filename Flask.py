from Recup_donnée_capteur import getTemp ,getHumidity , getPressure
from Adresseip import adresseIP
from flask import Flask ,render_template
from datetime import datetime, timedelta
import socket
import os
from pprint import pprint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib,email,email.encoders,email.mime.text,email.mime.base
from Database import insertValue,selectValue,deleteValue , deleteTable , createTable , selectSpecificValue
from templates_email import debut_email , end_email
# testsupervision2020@gmail.com
# testsupervision2!

# supervision.rasberry@gmail.com
# rasberrysupervision2020

# agash.pro@gmail.com , B.PALLIER@hotmail.fr , i.loubani89@gmail.com , gaetan.henriques@outlook.fr

app= Flask(__name__)

def sendEmail (text,type,etat):
	jour = datetime.now()
	heure = jour.hour
	minute = jour.minute
	value = selectValue()
	msg = MIMEMultipart()
	msg['From'] = 'supervision.rasberry@gmail.com'
	msg['To'] = 'i.loubani89@gmail.com'
	msg['Subject'] = 'Probleme Supervision Serveur '+type+' '+etat+' '+str(heure)+':'+str(minute)+'\n'
	message = debut_email()
	message = 'Bonjour !'+ '<br />'
	message += text
	message += '<br />'
	message += '<b>PROBLEME :</b>'+'<br />'
	if type== 'temperature':
		message += 'Le serveur possede un probleme sur la '+type+' '+str(getTemp())+'°C'
	elif type == 'Humidité':
		message += 'Le serveur possede un probleme sur l\''+type+' '+str(getHumidity())+' %'
	elif type == 'Pression':
		message += 'Le serveur possede un probleme sur la '+type+' '+str(getPressure())+' mBar'
	# message += '<br />'
	# message += 'Merci de reglé le probleme'
	# message += '<br />'
	# message += 'Florian Catinaud'
	message += end_email()
	msg.attach(MIMEText(message,'html'))
	mailserver = smtplib.SMTP('smtp.gmail.com', 587)
	mailserver.ehlo()
	mailserver.starttls()
	mailserver.ehlo()
	mailserver.login('supervision.rasberry@gmail.com', 'rasberrysupervision2020')
	mailserver.sendmail(msg['From'], msg['To'], msg.as_string())
	mailserver.quit()
	print('Envoie de mail à '+msg['To']+' '+str(type)+' '+str(etat))
	return

@app.route("/gT/<rep>")
def graTemp (rep):
	d=datetime.now()
	if rep == "temp":
		valeur = selectSpecificValue('temperature')
	elif rep == "humi":
		valeur = selectSpecificValue('pressure')
	elif rep == "press":
		valeur = selectSpecificValue('humidite')

	annee=str(d)[:4]
	titre =" Temperature actuelle : "+ str(getTemp())+ " °C"
	#strMonth = str(d.month)
	#strDay = str(d.day)
	#if len(strMonth) == 1:
	#	strMonth= "0" + strMonth
	#if len(strDay) == 1:
	#	strDay = "0" + strDay
	#dateTitle= strDay+"/"+strMonth+"/"+ str(d.year)
	#titre = "Statistiques du "+dateTitle

	ndate = d + timedelta(days=1)
	pdate = d - timedelta(days=1) 
	#tempMoy = str(round(moyenneListe(duree),1))
	#Moy = str(tempMoy[0])
	return render_template(
		'graphTemp.html',
		d = d.strftime("%Y-%m-%d"),
		titre = titre,
		temp = getTemp(),
		value = valeur,
		prevDate = ndate.strftime("%Y-%m-%d"),
		nextDate = pdate.strftime("%Y-%m-%d")
	)

@app.route("/")
def home():
	d= datetime.now()
	y = d.strftime('%Y-%m-%d')
	ndate = d + timedelta(days=1)
	pdate = d - timedelta(days=1)
	annee=str(d)[:4]
	jour=str(d)[:10]
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

	# -------------------- Supprimer les valeurs --------------------
	# deleteValue()

	# -------------------- Supprimer la table info --------------------
	# deleteTable()

	# -------------------- Creation de la table info --------------------
	# createTable()

	tableau = selectValue()
	return render_template(
		"home.html",
		title = "Supervision salle serveur",
		temp = getTemp(),
		humi = getHumidity(),
		press = getPressure(),
		value = tableau
		)

if __name__ =="__main__":
	app.run(debug=True,host=adresseIP(),port='5000')