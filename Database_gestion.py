import sqlite3

def SelectALlMail():
	conn = None
	valeur =[]
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'SELECT * FROM infoemail'
	# print("New valeur inserez")
	result = cur.execute(req)
	for row in result:
		valeur.append(row)
	conn.commit()
	conn.close()
	return valeur


def selectspecificMail(email):
	conn = None
	valeur =[]
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'SELECT email ,password,role FROM infoemail WHERE email ="'+email+'"'
	result = cur.execute(req)
	for row in result:
		valeur.append(row)
	conn.commit()
	conn.close()
	return valeur 

def InsertTableEmail(email,password, role):
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'INSERT INTO infoemail (email,password,role) VALUES ("'+email+'","'+password+'","'+role+'");'
	print("New valeur inserez in ImportanteValue in Table Email")
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
    password varchar,
    role varchar);'''
	# print("New valeur inserez")
	cur.execute(req)
	conn.commit()
	conn.close()
	return

def deleteOneEmail(idMail):
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	### Delete que un mail cree la requete !!!
	req = 'DELETE FROM infoemail where  id = "'+idMail+'" ; '
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
	valeur = []
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'SELECT * FROM seuilValue'
	result = cur.execute(req)
	for row in result:
		valeur.append(row)
	conn.commit()
	conn.close()
	return valeur

def CreateTableValue():
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	# Cree nouvelle colonne pour ajouter si ses MIN OU MAX 
	req = '''CREATE TABLE seuilValue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value varchar,
    etat varchar,
    type varchar);'''
	# print("New valeur inserez")
	cur.execute(req)
	conn.commit()
	conn.close()
	return

def insertTableValue(value,type,etat):
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	# Cree nouvelle colonne pour ajouter si ses MIN OU MAX 
	req = 'INSERT INTO seuilValue (value,type,etat) VALUES ("'+str(value)+'","'+type+'","'+etat+'");'
	# print("New valeur inserez")
	cur.execute(req)
	conn.commit()
	conn.close()
	return

def updateTableValue(value,id):
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	# Cree nouvelle colonne pour ajouter si ses MIN OU MAX 
	req = 'UPDATE seuilValue set value ="'+value+'" WHERE id='+id+';'
	print(req)
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

# ----------------------------------------------------------------------------------------------

def createTableLocalisation():
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = '''CREATE TABLE localisation (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		adresse varchar,
		nb int,
		name varchar)'''
	cur.execute(req)
	conn.commit()
	conn.close()
	return

def insertTableLocalsation(adresse,nb,name):
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'INSERT INTO localisation (adresse,nb,name) VALUES("'+str(adresse)+'","'+nb+'","'+name+'");'
	cur.execute(req)
	conn.commit()
	conn.close()
	return

def updateTableLocalisation(adresse,nb,name,id):
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'UPDATE localisation set adresse ="'+adresse+'",nb='+nb+',name="'+name+'" WHERE id='+id+';'
	cur.execute(req)
	conn.commit()
	conn.close()
	return

def SelectLocalisation():
	valeur = []
	conn = None
	try :
		conn = sqlite3.connect('ImportanteValue.db')
	except Error as e:
		print(e)
	cur = conn.cursor()
	req = 'SELECT * FROM localisation WHERE id=1'
	result = cur.execute(req)
	for row in result:
		valeur.append(row)
	conn.commit()
	conn.close()
	return valeur