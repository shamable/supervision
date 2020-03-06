import sqlite3

"""
conn = sqlite3.connect('supervision.db')
cur = conn.cursor()
req = "select Pression, Humidite, Temperature from Infos"
result = cur.execute(req)
for row in result:
	print(type(row))
"""
def insertValue(temp,press,humi):
	conn = None
	try :
		conn = sqlite3.connect('supervision.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'INSERT INTO info (jour,horaire,temperature,pressure,humidite) VALUES (date("now"),time("now"),'+temp+','+press+','+humi+');'
	cur.execute(req)
	conn.commit()
	conn.close()
	return

def selectValue():
	valeur = []
	conn = sqlite3.connect('supervision.db')
	cur = conn.cursor()
	req = "SELECT id, pressure, humidite, temperature,strftime('%H:%M',horaire),strftime('%d-%m-%Y',jour) FROM info"
	result = cur.execute(req)
	for row in result:
		#print('Row '+str(row))
		valeur.append(row)
	#print(valeur)
	return valeur
def selectSpecificValue(value):
	valeur = []
	conn = sqlite3.connect('supervision.db')
	cur = conn.cursor()
	req = "SELECT "+value+",strftime('%H:%M',horaire) FROM info"
	result = cur.execute(req)
	for row in result:
		valeur.append(row)
		# print('select specific value Row '+str(row))
	# print(valeur)
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