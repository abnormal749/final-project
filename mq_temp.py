#!/usr/bin/python
import subprocess, time, sys
import Adafruit_DHT
import paho.mqtt.client as mqtt
from time import gmtime,strftime

### custom action ###
def on_connect(client, userdata, flags, rc):
     print("Connected code: {}".format(rc))
     client.subscribe(topic = "test")
def on_disconnect(client, userdata, rc):
	print("Disconnected From Broker")
def on_message(client, userdata, message):
    print("message received: " ,str(message.payload.decode("utf-8")))
    print("message topic:\t  ",message.topic)
    print("message qos:\t  ",message.qos)
    print("retain flag:\t  ",message.retain)
### action appointed ###
print("creating new instance")
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

print("connecting to broker")
client.connect("140.123.107.170",1883,60)
time.sleep(0.5)
client.loop_start()
###------------------###
sensor = Adafruit_DHT.AM2302
pin = 4

cmd = "(vcgencmd measure_temp)"

while True:
	try:
		out = subprocess.check_output(cmd,shell=True)
		out = float(out[5:9])
		print("CPU temp: ",out)

		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

		if humidity is not None and temperature is not None:
			print('Temp    :  {0:.2f}'.format(temperature))
			print('Humidity:  {0:.2f}%'.format(humidity))

		humidity = round(humidity,2)
		temperature = round(temperature,2)
		datt  = strftime("%Y%m%d")
		timm  = strftime("%H%M%S")
		timee = (datt + timm)
		#timee = timee.replace(' ','')

		sendy = "'EE'  {}  {}  {}  {}".format(out,temperature,humidity,timee)
		client.publish("sen/temp",sendy)

		print("{} {}".format(datt,timm))
		print(timee)
		print("------------------")
		time.sleep(5)

	except KeyboardInterrupt:
		client.loop_stop()
		break
