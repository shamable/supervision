from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
# Si erreur sur cette ligne la allez dans le terminale et tapez "pip install MIMEMultipart"
from email.mime.text import MIMEText
import smtplib

# Include de mes fichiers avec mes def
from Recup_donnée_capteur import getTemp ,getHumidity , getPressure
from Database import insertValue , selectValue,deleteValue , deleteTable , createTable , selectSpecificValue
from Database_gestion import SelectALlMail
from templates_email import debut_email , end_email
# Vous ne possedez pas le fichier login_email.py
# Pour des raisons de securite
from login_email import email,emailMDP, email_TO

def sendEmail (text,type,etat):
	jour = datetime.now()
	heure = jour.hour
	minute = jour.minute
	value = selectValue(False)
	msg = MIMEMultipart()
	msg['From'] = email()
	
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
	message += '<br />'
	message += 'Merci de reglé le probleme'
	message += '<br />'
	message += 'Florian Catinaud'
	message += end_email()
	msg.attach(MIMEText(message,'html'))
	mailserver = smtplib.SMTP('smtp.gmail.com', 587)
	mailserver.ehlo()
	mailserver.starttls()
	mailserver.ehlo()
	mailserver.login(email(),emailMDP())
	# SI probleme a la ligne 41 c'esst normal 
	# J'ai mis les mails dans un fichier a part que je ne mais pas dans le git
	# Pour raison de securité
	valeur = SelectALlMail()
	#print(valeur)
	for row in valeur :
		to = row[1]
		mailserver.sendmail(msg['From'], to, msg.as_string())
		print('Envoie de mail à '+to+' '+str(type)+" "+str(etat))
	mailserver.quit()
	return