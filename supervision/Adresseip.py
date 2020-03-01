import socket

def adresseIP():
	hostname = socket.gethostname()
	ip = socket.gethostbyname(hostname)
	var = ip
	return var