import paho.mqtt.client as mqtt # install with pip3 install paho-mqtt
import json


def connect_mqtt(temp,humi,press):
	d=datetime.now()
	channel = "test_channel"

	data_send={"Temperature": temp ,"Humidity" : humi ,"Pressure" : press}
	client = mqtt.Client()

	client.loop_start()
	client.connect("192.168.1.27",1883,60)# Avoir l'adresse ip de l'autre machine 
	if client:
	#while True : 
		client.subscribe(channel)
		client.publish(channel,json.dumps(data_send),1)
		print("MQTT send : " +str(data_send))

	client.loop_stop()
	client.disconnect()
	return
