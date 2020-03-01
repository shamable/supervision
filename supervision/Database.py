import sqlite3
conn = sqlite3.connect('Supervision.db')
cur = conn.cursor()
req = "select Pression, Humidite, Temperature from Infos"
result = cur.execute(req)
for row in result:
	print(type(row))

	
"""conn = sqlite3.connect('Supervision.db')
cur = conn.cursor()
cur.execute("PRAGMA table_info (Infos);")
print(cur.fetchall())"""