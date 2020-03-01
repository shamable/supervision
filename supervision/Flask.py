from Recup_donnée_capteur import getTemp ,getHumidity , getPressure
from Adresseip import adresseIP
from flask import Flask ,render_template
from datetime import datetime, timedelta
import socket
import os
from pprint import pprint
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEText import MIMEText
import smtplib,email,email.encoders,email.mime.text,email.mime.base


app= Flask(__name__)

def sendEmail ():
    # *msg = MIMEMultipart()
    # msg['From'] = 'TestSupervision2020@gmail.com'
    # msg['To'] = 'catinaud.florian@gmail.com'
    # msg['Subject'] = 'Probleme Supervision Serveur' 
    # message = 'Bonjour !'
    # msg.attach(MIMEText(message))
    # mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    # mailserver.ehlo()
    # mailserver.starttls()
    # mailserver.ehlo()
    # mailserver.login('TestSupervision2020@gmail.com', 'TestSupervision2%')
    # mailserver.sendmail(msg['From'], msg['To'], msg.as_string())
    # mailserver.quit()
    
    smtpserver = 'TestSupervision2020@gmail.com'
    to = ['catinaud.florian@gmail.com']
    fromAddr = 'TestSupervision2020@gmail.com'
    subject = "Probleme Supervision Server TEST"
    
    # create html email
    html = '<!DOCTYPE html>'
    html +='<body style="font-size:12px;font-family:Verdana"><p>CECI EST UN TEST</p>'
    html += "</body></html>"
    emailMsg = email.MIMEMultipart.MIMEMultipart('text/csv')
    emailMsg['Subject'] = subject
    emailMsg['From'] = fromAddr
    emailMsg['To'] = ', '.join(to)
    emailMsg['Cc'] = ", ".join(cc)
    emailMsg.attach(email.mime.text.MIMEText(html,'html'))
    
    # now attach the file
    fileMsg = email.mime.base.MIMEBase('text/csv')
    fileMsg.set_payload(file('rsvps.csv').read())
    email.encoders.encode_base64(fileMsg)
    fileMsg.add_header('Content-Disposition','attachment;filename=rsvps.csv')
    emailMsg.attach(fileMsg)
    
    # send email
    server = smtplib.SMTP(smtpserver)
    server.sendmail(fromAddr,to,emailMsg.as_string())
    server.quit()
    

def enregistrement (repertoire, valeur):
	date=datetime.now()
	annee=str(date)[:4]
	jour=str(date)[:10]

	repertoire = repertoire +'/'+ annee+'/'

	if not os.path.isdir(repertoire):
		os.makedirs(repertoire)

	fiche = repertoire + jour+ '.txt'

	if os.path.exists(fiche):
		f=open(fiche,"a")
		
	else:
		f=open(fiche,"w")
	time=date.strftime("%H,%M")
	print(str(time)+" "+str(valeur),file=f)
	f.close
	return str(valeur)

def fichierVersListe(repertoire):
	date=datetime.now()
	annee=str(date)[:4]
	jour=str(date)[:10]
	points = []
	temp = []
	f= open(repertoire+"/"+annee+"/"+jour+".txt", "r")

	for line in f :
		points.append(line[0:2]+":"+line[3:5]+"_"+line[6:len(line)-1])
		print(points)
	f.close()
	print(points)
	return points


def moyenneListe(liste):
	res = 0 
	for i in liste:
		res+=i
	return res/len(liste)

@app.route("/gT/<date>/<rep>")
def graTemp (date,rep):
	i = 0
	j = 0
	heure =[]
	value = []
	test=[]
	allHeure=[]
	allValue=[]
	tem = "temp"
	hum = "humi"
	pres = "press"
	d=datetime.now()  
	if rep == tem:
		rep = '/home/pi/Documents/Flask/temperature'
	elif rep == hum:
		rep = '/home/pi/Documents/Flask/humidity'
	elif rep == pres:
		rep = '/home/pi/Documents/Flask/pressure'
	if date is None: 
		annee=str(d)[:4]
		titre =" Temperature actuelle : "+ str(getTemp())+ " °C"
	else :
		strMonth = str(d.month)
		strDay = str(d.day)
		if len(strMonth) == 1:
			strMonth= "0" + strMonth
		if len(strDay) == 1:
			strDay = "0" + strDay
		dateTitle= strDay+"/"+strMonth+"/"+ str(d.year)
		titre = "Statistiques du "+dateTitle

	pointsAndTemp = fichierVersListe(rep)
	while i < len(pointsAndTemp):
		split=pointsAndTemp[i].split("_")
		value=split[1]
		heure=split[0]
		i=i+1
		allHeure.append(heure)
		allValue.append(value)

	while j < len(pointsAndTemp):
		splitdeu = pointsAndTemp[j].split("'_'")
		allValue += splitdeu
		pass
	y=allHeure
	nbValue=len(allValue);

	ndate = d + timedelta(days=1)
	pdate = d - timedelta(days=1) 
	#tempMoy = str(round(moyenneListe(duree),1))
	#Moy = str(tempMoy[0])
	return render_template(
		'graphTemp.html',
		d = d.strftime("%Y-%m-%d"),
		y1=y,
		nbValue=nbValue,
		heure=allHeure,
		valeur=allValue,
		y= pointsAndTemp,
		titre = titre,
		temp = getTemp(),
		# -------------------------------------
		# tempMin=round(min(duree),1),
		# tempMax = round(max(duree),1),
		# tempMoy = Moy,
		# -------------------------------------
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

	print(getTemp())
    
    #if getTemp() == getTemp():
    sendEmail()
     
    #if getTemp() > '80': 
    #    sendEmail()
    #elif (getTemp() < '10') :
    #    sendEmail()
    #if getHumidity() > '80' || getHumidity() < '5' : 
    #    sendEmail()
    #if getPressure() > '1000' || getPressure() < '300' :     
    #    sendEmail()
    
	return render_template(
		"home.html",
		title = "Supervision salle serveur",
		temp = enregistrement('/home/pi/Documents/Flask/temperature',getTemp()),
		humi = enregistrement('/home/pi/Documents/Flask/humidity',getHumidity()),
		press = enregistrement('/home/pi/Documents/Flask/pressure',getPressure())#,
		#y= temps#,tempMin,
		#y2 = temp,
		#y4 = pointsAndTemp#,
		#y5 = ndate.strftime("%Y-%m-%d"),
		#y6 = pdate.strftime("%Y-%m-%d"),
		#y7 = fichierVersListe('/home/pi/Documents/Flask/temperature')
		# test = fichierVersListe(RepTemp())
		)


if __name__ =="__main__":
	app.run(debug=True,host=adresseIP(),port='5000')