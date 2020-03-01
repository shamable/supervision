from sense_emu import SenseHat
sense= SenseHat()
def getTemp():
	temp=sense.get_temperature()
	return temp
	
def getHumidity():
	humi=sense.get_humidity()
	return humi

def getPressure():
	Press=sense.get_pressure()
	return Press