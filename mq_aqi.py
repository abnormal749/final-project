import serial,datetime,time
import paho.mqtt.client as mqtt
from time import gmtime,strftime

port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)

def read_pm_line():
  rv = b''
  while True:
    ch1 = port.read(2)
    #print("get 1: {}".format(ch1))
    if ch1 == b'\x42\x4D':
        rv += port.read(30)
        return rv
### custom action ###
def on_connect(client, userdata, flags, rc):
     print("Connected code: {}".format(rc))
     client.subscribe(topic = "test")
def on_disconnect(client, userdata, rc):
        print("Disconnected From Broker")
### action appointed ###
print("creating new instance")
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect

print("connecting to broker")
client.connect("140.123.107.170",1883,60)
time.sleep(0.5)
client.loop_start()

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
    datt  = strftime("%Y%m%d")
    timm  = strftime("%H%M%S")
    timee = datt + timm
    print(timee)
    msg = "'EE'  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}".format(res['pm10'],res['pm25'],res['pm100'],res['gt03um'],res['gt05um'],res['gt10um'],res['gt25um'],res['gt50um'],res['gt100um'],timee)
    client.publish("sen/aqi",msg)
    time.sleep(5)

  except KeyboardInterrupt:
    client.loop_stop()
    break

