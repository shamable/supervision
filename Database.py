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
	req = 'INSERT INTO info (horaire,temperature,pressure,humidite) VALUES (date("now"),'+temp+','+press+','+humi+');'
	cur.execute(req)
	conn.commit()
	conn.close()
	return

def selectValue():
	valeur = []
	conn = sqlite3.connect('supervision.db')
	cur = conn.cursor()
	req = "select id, pressure, humidite, temperature from info"
	result = cur.execute(req)
	for row in result:
		#print('Row '+str(row))
		valeur.append(row)
	#print(valeur)
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
    horaire datetime,
    temperature float,
    pressure float,
    humidite int);'''
	cur.execute(req)
	conn.commit()
	conn.close()
	return