from sense_emu import SenseHat
sense= SenseHat()
def getTemp():
	temp=sense.get_temperature()
	return int(temp)
	
def getHumidity():
	humi=sense.get_humidity()
	return int(humi)

def getPressure():
	Press=sense.get_pressure()
	return int(Press)