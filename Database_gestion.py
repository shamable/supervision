import sqlite3

# Definition permettant de recuperer les adresse mails en tant que admin pour pouvoir les supprimer au besoin
def SelectALlMail():
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'SELECT * FROM infoemail'
	# print("New valeur inserez")
	cur.execute(req)
	conn.commit()
	conn.close()
	return


def selectspecificMail(email):
	conn = None
	valeur =[]
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'SELECT email ,password FROM infoemail WHERE email ="'+email+'"'
	result = cur.execute(req)
	for row in result:
		valeur.append(row)
	conn.commit()
	conn.close()
	return valeur 

def InsertTableEmail(email,password):
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'INSERT INTO infoemail (email,password) VALUES ("'+email+'","'+password+'");'
	print('INSERT INTO infoemail (email,password) VALUES ("'+email+'","'+password+'");')
	print("New valeur inserez in ImportanteValue in Table Email")
	print("--------------------------------------------")
	print("email : "+email +" password : "+password)
	cur.execute(req)
	conn.commit()
	conn.close()
	return

def CreateTableEmail():
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = '''CREATE TABLE infoemail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email varchar,
    password varchar);'''
	# print("New valeur inserez")
	cur.execute(req)
	conn.commit()
	conn.close()
	return


def deleteTableEmail():
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = '''DROP TABLE infoemail ; '''
	# print("New valeur inserez")
	cur.execute(req)
	conn.commit()
	conn.close()
	return

# ----------------------------------------------------------------------------------------
# Requete pour la table Seuil 
def SelectSeuilValue():
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'SELECT * FROM seuilValue'

	cur.execute(req)
	conn.commit()
	conn.close()
	return

# Creer la def pour l'instertion de valeur et ensutie la modification 


def CreateTableValue():
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = '''CREATE TABLE seuilValue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value int,
    type text);'''
	# print("New valeur inserez")
	cur.execute(req)
	conn.commit()
	conn.close()
	return

def deleteTableValue():
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = '''DROP TABLE seuilValue ; '''
	# print("New valeur inserez")
	cur.execute(req)
	conn.commit()
	conn.close()
	return