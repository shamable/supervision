import os
from Database import insertValue
from envoie_mail import sendEmail
from Recup_donnée_capteur import getTemp ,getHumidity , getPressure
from Database_gestion import SelectALlMail,CreateTableEmail,deleteTableEmail , SelectSeuilValue , CreateTableValue, deleteTableValue, InsertTableEmail,selectspecificMail,deleteOneEmail,insertTableValue ,updateTableValue
import time 
from datetime import datetime
i=0

def insertfivemin():
	insertValue(str(getTemp()),str(getPressure()),str(getHumidity()))
	valeur = SelectSeuilValue()
	for row in valeur :
		if row[0] == 1 :
			if int(getTemp()) < int(row[1]) :
				sendEmail('Temperature Trop basse','temperature','basse')
		if row[0] == 2 : 
			if int(getTemp()) > int(row[1]) :
				sendEmail('Temperature Trop haute','temperature','haute')
		if row[0] == 3 :
			if int(getPressure()) < float(row[1]) :
				sendEmail('Pression Trop basse','Pression','basse')
		if row[0] == 4 : 
			if int(getPressure()) > float(row[1]) :
				sendEmail('Pression Trop haute','Pression','haute')
		if row[0] == 5 :
			if int(getHumidity()) < int(row[1]) :
				sendEmail('Humidité Trop basse','Humidité','basse')
		if row[0] == 6 : 
			if int(getHumidity()) > int(row[1]) :
				sendEmail('Humidité Trop haute','Humidité','haute')
	return

while i >= 0 : 
	t = datetime.now()
	print("i  = "+str(i)+"  time  : "+str(t))
	time.sleep(300)
	insertfivemin()
	i+=1
