from mqtt import connect_mqtt
import sqlite3

def insertValue(temp,press,humi):
	# connect_mqtt(temp,humi,press)
	conn = None
	try :
		conn = sqlite3.connect('supervision.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	# Probleme avec SQL sur l'horaire 
	req = 'INSERT INTO info (jour,horaire,temperature,pressure,humidite) VALUES (date("now"),time("now"),'+temp+','+press+','+humi+');'
	print("New valeur inserez")
	cur.execute(req)
	conn.commit()
	conn.close()
	return

def selectValue(debug):
	valeur = []
	conn = sqlite3.connect('supervision.db')
	cur = conn.cursor()
	req = "SELECT id, pressure, humidite, temperature,strftime('%H:%M',horaire) as horaire,strftime('%d-%m-%Y',jour) as jour FROM info WHERE jour = date('now')ORDER BY jour DESC, horaire DESC ;"
	result = cur.execute(req)
	for row in result:
		if debug : 
			print('Row '+str(row))
		valeur.append(row)
	conn.close()
	return valeur


def selectAllValue(debug):
	valeur = []
	conn = sqlite3.connect('supervision.db')
	cur = conn.cursor()
	req = "SELECT id, pressure, humidite, temperature,strftime('%H:%M',horaire) as horaire,strftime('%d-%m-%Y',jour) as jour FROM info ORDER BY jour DESC, horaire DESC ;"
	result = cur.execute(req)
	for row in result:
		if debug : 
			print('Row '+str(row))
		valeur.append(row)
	conn.close()
	return valeur


def selectSpecificValue(value,date):
	valeur = []
	conn = sqlite3.connect('supervision.db')
	cur = conn.cursor()
	req = "SELECT "+value+",strftime('%H:%M',horaire) FROM info WHERE jour = '"+date+"'"
	result = cur.execute(req)
	for row in result:
		valeur.append(row)
	conn.close()
	return valeur

def deleteValue():
	try :
		conn = sqlite3.connect('supervision.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'DELETE FROM info WHERE id <100;'
	cur.execute(req)
	conn.commit()
	conn.close()
	return

def deleteTable():
	try :
		conn = sqlite3.connect('supervision.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'DROP TABLE info ;'
	cur.execute(req)
	conn.commit()
	conn.close()
	return

def createTable():
	try :
		conn = sqlite3.connect('supervision.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = '''CREATE TABLE info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jour datetime,
    horaire time,
    temperature float,
    pressure float,
    humidite int);'''
	cur.execute(req)
	conn.commit()
	conn.close()
	return