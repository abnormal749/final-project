from opcua import Client
import time, serial,datetime, sys
import Adafruit_DHT
from time import gmtime,strftime

# pms5003------------------------------
port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)

def read_pm_line():
  rv = b''
  while True:
    ch1 = port.read(2)
    #print("get 1: {}".format(ch1))
    if ch1 == b'\x42\x4D':
        rv += port.read(30)
        return rv
# ASAIR -------------------------------
sensor = Adafruit_DHT.AM2302
pin = 4

# opc connect -------------------------
url = "opc.tcp://140.123.107.170:31905"
client = Client(url)

client.connect()
print("Client connect")
time.sleep(1)

# main --------------------------------
while True:
	try:
		rcv = read_pm_line()
		res = {'timestamp':datetime.datetime.now()}
		res['apm10']=(rcv[2] * 256 + rcv[3])
		res['apm25']=(rcv[4] * 256 + rcv[5])
		res['apm100']=(rcv[6] * 256 + rcv[7])
		res['pm10']=(rcv[8] * 256 + rcv[9])
		res['pm25']=(rcv[10] * 256 + rcv[11])
		res['pm100']=(rcv[12] * 256 + rcv[13])
		res['gt03um']=(rcv[14] * 256 + rcv[15])
		res['gt05um']=(rcv[16] * 256 + rcv[17])
		res['gt10um']=(rcv[18] * 256 + rcv[19])
		res['gt25um']=(rcv[20] * 256 + rcv[21])
		res['gt50um']=(rcv[22] * 256 + rcv[23])
		res['gt100um']=(rcv[24] * 256 + rcv[25])
		print("===============")
		print("PM1\t: {}".format(res['pm10']))
		print("PM2.5\t: {}".format(res['pm25']))
		print("PM10\t: {}".format(res['pm100']))
		print(">0.3um\t: {}".format(res['gt03um']))
		print(">0.5um\t: {}".format(res['gt05um']))
		print(">1.0um\t: {}".format(res['gt10um']))
		print(">2.5um\t: {}".format(res['gt25um']))
		print(">5.0um\t: {}".format(res['gt50um']))
		print(">10um\t: {}".format(res['gt100um']))

		pm1 = client.get_node("ns=2;i=17")
		pm25 = client.get_node("ns=2;i=18")
		pm10 = client.get_node("ns=2;i=19")
		um3 = client.get_node("ns=2;i=20")
		um5 = client.get_node("ns=2;i=21")
		um10 = client.get_node("ns=2;i=22")
		um25 = client.get_node("ns=2;i=23")
		um50 = client.get_node("ns=2;i=24")
		um100 = client.get_node("ns=2;i=25")

		pm1.set_value(res['pm10'])
		pm25.set_value(res['pm25'])
		pm10.set_value(res['pm100'])
		um3.set_value(res['gt03um'])
		um5.set_value(res['gt05um'])
		um10.set_value(res['gt10um'])
		um25.set_value(res['gt25um'])
		um50.set_value(res['gt50um'])
		um100.set_value(res['gt100um'])

        	out = subprocess.check_output(cmd,shell=True)
		out = float(out[5:9])
		print("CPU temp: ",out)

		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

		if humidity is not None and temperature is not None:
			print('Temp    :  {0:.2f}'.format(temperature))
			print('Humidity:  {0:.2f}%'.format(humidity))

		humidity = round(humidity,2)
		temperature = round(temperature,2)
		timm = strftime("%H:%M:%S")

		core_temp = client.get_node("ns=2;i=3")
		su_temp = client.get_node("ns=2;i=4")
		su_humd = client.get_node("ns=2;i=5")
		timee = client.get_node("ns=2;i=6")

		core_temp.set_value(out)
		su_temp.set_value(temperature)
		su_humd.set_value(humidity)
		timee.set_value(timm)

		time.sleep(5)
	except KeyboardInterrupt:
		break
