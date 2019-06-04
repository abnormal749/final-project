import time, sys, os
sys.path.append('/home/st2019e/pah0')
import paho.mqtt.client as mqtt

# code for server(140.123.107.170)
############
def on_message1(client, userdata, message):
    print('Temp received: ',str(message.payload.decode("utf-8")))
    items_list = message.payload.decode("utf-8").replace("  ",",")
    #items_list = items_list.replace('-','')
    #items_list = items_list.replace(':','')
    items = """{} """.format(items_list)
    os.system('mysql --defaults-extra-file=/home/st2019e/profile.cnf -Dst2019e -e"INSERT INTO rasp_temp2(device_name,core_temp,su_temp,su_humid,time) VALUES(%s)"'%(items))
def on_message2(client, userdata, message):
    print('AQI  received: ',str(message.payload.decode("utf-8")))
    items_list = message.payload.decode("utf-8").replace("  ",",")
    #items_list = items_list.replace('-','')
    #items_list = items_list.replace(':','')
    items = """{} """.format(items_list)
    os.system('mysql --defaults-extra-file=/home/st2019e/profile.cnf -Dst2019e -e"INSERT INTO rasp_aqi2(device_name,pm_10,pm_25,pm_100,03um,05um,10um,25um,50um,100um,time) VALUES(%s)"'%(items))
############

print("creating new instance...")
cli_temp = mqtt.Client()
cli_aqi  = mqtt.Client()
cli_temp.on_message = on_message1
cli_aqi.on_message  = on_message2

print("connecting to broker...")
cli_temp.connect("127.0.0.1",1883,60)
cli_aqi.connect("127.0.0.1",1883,60)

cli_temp.loop_start()
cli_aqi.loop_start()
time.sleep(0.5)

print("Subscribing to topic : sen/temp  sen/aqi")
cli_temp.subscribe("sen/temp")
cli_aqi.subscribe("sen/aqi")
print("-------------------------------")

while True:
	try:
		time.sleep(3)
	except KeyboardInterrupt:
		cli_temp.loop_stop()
		cli_aqi.loop_stop()
		break
