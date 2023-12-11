#!/usr/bin/env python3
# need installed:
# pip3 install paho-mqtt

# revision with using .env file
# pip3 install python-dotenv

# Copyright 2021 HiveMQ GmbH
import paho.mqtt.client as paho
from paho import mqtt
# MOD KLL 2022-12-15
# rev 1.1.2b2 in PICO W
# rev 1.1.3b4 topic change
# rev 1.2.3 c NTP
# rec 1.2.3 e python in venv and new TOPIC structure

import time
from datetime import datetime
from dotenv import load_dotenv
import os # ,sys,shutil
encoding = 'utf-8'
import json


load_dotenv()

R_broker_ip=os.getenv('remote_clusterURL')
R_port=int(os.getenv('remote_port') )
R_user=os.getenv('remote_MQTT_user')
R_pwd=os.getenv('remote_MQTT_pass')
# REMOTE TOPIC and MQTT CLIENT must be unique
R_mtopic=os.getenv('remote_mtopic') # 'PICOW-S31' # resembles our data structure / main header
R_dtopic=os.getenv('remote_dtopic') # the site the data come from
R_topic=R_mtopic+'/'+R_dtopic

L_broker_ip=os.getenv('MQTT_broker')
L_port=int(os.getenv('MQTT_port') )
L_user=os.getenv('MQTT_user')
L_pwd=os.getenv('MQTT_pass')
L_mtopic=os.getenv('MQTT_mtopic')
L_dtopic=os.getenv('MQTT_dtopic')
L_S31topic=os.getenv('MQTT_S31topic')

L_topic_PICOW=L_mtopic+'/'+L_dtopic
L_topic_S31=L_S31topic


startt = datetime.now() # local RPI time
count = 0

# python all variables from 2 payloads:
# PICO_W
LP_lastt = startt
LP_id = 0
LP_tnows = ''
LP_dev = 'P00'
LP_Temp = 0.0
LP_Volt = 0.0
LP_Amp = 0.0
LP_Watt = 0.0

# PICO_W S31 Tasmota
LS_lastt = startt
LS_Time = " "
# ENERGY:{}
LS_TotalStartTime = " "
LS_Total = 0.0
LS_Yesterday = 0.0
LS_Today = 0.0
LS_Period = 0
LS_Power = 0.0
LS_ApparentPower = 0.0
LS_ReactivePower = 0.0
LS_Factor = 0.0
LS_Voltage = 0.0
LS_Current = 0.0


def Split_payload(nowt, topic, payload) : # ____________________________ nowt is local time at RPI when that data came in from RPI broker sub
	global LP_lastt, LP_id, LP_tnows, LP_dev, LP_Temp, LP_Volt, LP_Amp, LP_Watt
	global LS_lastt, LS_Time, LS_TotalStartTime, LS_Total, LS_Yesterday, LS_Today, LS_Period
	global LS_Power, LS_ApparentPower, LS_ReactivePower, LS_Factor, LS_Voltage, LS_Current
	if ( topic == L_topic_PICOW ) :
		#print("+++ from PICO W:")
		LP_lastt = nowt
		#STRs = payload.decode("utf-8")
		#JSONs = STRs.replace("\'","\"") #  for real JSON must use " , NOT ' like i use in PICO W > broker > Node-Red > SQLIte save db
		JSONs = payload.decode("utf-8")
		data = json.loads(JSONs)
		LP_id = data.get("id",{})
		LP_tnows = data.get("datetimes",{}) # rev 1.2.3 c
		LP_dev = data.get("dev",{})
		LP_Temp = data.get("PS_Temp",{}) # rev 1.1.3 b4
		# v1.1.2.b2
		LP_Volt = data.get("DC_Volt",{})
		LP_Amp = data.get("DC_Amp",{})
		LP_Watt = data.get("DC_Watt",{})
		print ("+++ from PICO W: lastt",LP_lastt.strftime("%Y_%m_%d_%H_%M_%S"),"id",LP_id,"datetimes",LP_tnows,"dev",LP_dev,"PS_Temp",LP_Temp,"DC_Volt",LP_Volt,"DC_Amp",LP_Amp,"DC_Watt",LP_Watt)
	elif ( topic == L_topic_S31 ) :
		LS_lastt = nowt
		JSONs = payload.decode("utf-8")
		data = json.loads(JSONs)
		LS_Time = data.get("Time",{})
		dataENERGY = data["ENERGY"] # should be new object
		LS_TotalStartTime = dataENERGY.get("TotalStartTime",{})
		LS_Total = dataENERGY.get("Total",{})
		LS_Yesterday = dataENERGY.get("Yesterday",{})
		LS_Today = dataENERGY.get("Today",{})
		LS_Period = dataENERGY.get("Period",{})
		LS_Power = dataENERGY.get("Power",{})
		LS_ApparentPower = dataENERGY.get("ApparentPower",{})
		LS_ReactivePower = dataENERGY.get("ReactivePower",{})
		LS_Factor = dataENERGY.get("Factor",{})
		LS_Voltage = dataENERGY.get("Voltage",{})
		LS_Current = dataENERGY.get("Current",{})
		print("+++ from S31:lastt",LS_lastt.strftime("%Y_%m_%d_%H_%M_%S"),"Time",LS_Time,"Voltage",LS_Voltage,"Current",LS_Current,"Power",LS_Power)
	else :
		print ("where that come from? ",topic)



def L_on_connect(mqttc, obj, flags, rc):
	if ( rc == 0 ) :
		print("___+ LOCAL connect OK")
		print("+++ listen to "+L_topic_PICOW+" and "+L_topic_S31 )

	else :
		print("___- LOCAL not connect rc: "+str(rc))

def R_on_connect(mqttc, obj, flags, rc):
	if ( rc == 0 ) :
		print("___+ REMOTE connect OK")
	else :
		print("___- REMOTE not connect rc: "+str(rc))

def L_on_message(mqttc, obj, msg):
	nowt = datetime.now()
	#dtsf = nowt.strftime("%Y_%m_%d_%H_%M_%S")
	#print("___ LOCAL " + dtsf + " " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
	Split_payload(nowt,msg.topic,msg.payload)


def R_on_message(mqttc, obj, msg):
	nowt = datetime.now()
	dtsf = nowt.strftime("%Y_%m_%d_%H_%M_%S")
	print("___ REMOTE " + dtsf + " " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
	# ? expect commands from REMOTE ? S31 ON OFF

def on_publish(mqttc, obj, mid): # _____________________________________ this prints after publish, but actually before next line print!
	print("___+ published mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
	print("___+ subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
	print(string)

print("___ connect to HIVEMQ.com free developer account and 1 min BRIDGE: send local data")
startt = datetime.now()
print("___ start: ",startt)

#mqttR = paho.Client(client_id="py_bridge", userdata=None, protocol=paho.MQTTv311)
mqttR = paho.Client(client_id=R_dtopic, userdata=None, protocol=paho.MQTTv311)
mqttR.username_pw_set(username=R_user,password=R_pwd) # ________________ HIVEMQ credentials
mqttR.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS) # ______________ with account must use TLS and 8883
mqttR.on_message = R_on_message
mqttR.on_connect = R_on_connect
mqttR.on_publish = on_publish
mqttR.on_subscribe = on_subscribe
# mqttR.on_log = on_log
R_good = False
try:
	mqttR.connect(R_broker_ip, R_port)
	R_good = True
	#print("--- Remote mqtt broker connect "+)
except:
	print("--- Remote mqtt broker NOT connect")


#mqttR.subscribe((R_topic, 0)) # ________________________________________ get back data from HIVEMQ send by local bridge
#mqttR.loop_forever()

mqttL = paho.Client("py_local_RPI")
mqttL.username_pw_set(username=L_user,password=L_pwd) # ________________ as we use RPI Mosquitto2 streamsheets with this connector
mqttL.on_message = L_on_message
mqttL.on_connect = L_on_connect
mqttL.on_publish = on_publish
mqttL.on_subscribe = on_subscribe
# mqttL.on_log = on_log
L_good = False

def local_sub() :
	global L_good
	try:
		mqttL.connect(L_broker_ip, L_port, 60)
		L_good = True
		mqttL.subscribe([(L_topic_PICOW, 0),(L_topic_S31, 0)]) # _______________ get data from PICO_W and S31
	except:
		print("--- Local mqtt broker NOT connect")

local_sub()


lastt = datetime.now()

def reset_analog_values():
	global LP_lastt, LP_id, LP_dev, LP_Temp, LP_Volt, LP_Amp, LP_Watt
	global LS_lastt, LS_Time, LS_TotalStartTime, LS_Total, LS_Yesterday, LS_Today, LS_Period
	global LS_Power, LS_ApparentPower, LS_ReactivePower, LS_Factor, LS_Voltage, LS_Current
	Nval=-0.007
	LS_Voltage=Nval
	LS_Current=Nval
	LS_Power=Nval
	LP_Temp=Nval
	LP_Volt=Nval
	LP_Amp=Nval
	LP_Watt=Nval

reset_analog_values() # ________________________________________ in case next minute no NEW subscribed data come in show -0.007

def send_to_remote() :
	global R_good, L_good, count
	if ( L_good != True ) : local_sub() # ______________________________ local data connection check
	#print("firt program start_ was:",startt.strftime("%Y_%m_%d_%H_%M_%S") )
	#print("last remote send___ was:",lastt.strftime("%Y_%m_%d_%H_%M_%S") )
	#print("last local picow in was:",LP_lastt.strftime("%Y_%m_%d_%H_%M_%S") )
	#print("last local S31__ in was:",LS_lastt.strftime("%Y_%m_%d_%H_%M_%S") )
	#print("and NOW is ____________:",nowt.strftime("%Y_%m_%d_%H_%M_%S") )
	# __________________________________________________________________ open point time check and UTC/local time ?
	# __________________________________________________________________ build new send record to remote broker 
	datas =  "{"
	datas += f" \"id\": {count},"
	datas += " \"minute\": "+str(nowt.minute)+"," # ____________________ so can check if BRIDGE send out local mqtt in a minute

	datas += " \"datetime\": "+LP_lastt.utcnow().strftime("%s") +"," # _ use time of data from PICOW come in (local RPI time to UTC epoch)
	#datas += " \"datetimes\": \""+LP_lastt.strftime("%Y_%m_%d_%H_%M_%S")+"\"," # LOCAL TIME of mqtt PICO W incoming
	datas += " \"datetimes\": \""+LP_tnows+"\"," # LOCAL TIME of mqtt PICO W use NTP incoming

	datas += " \"AC_Volt\": "+f"{float(LS_Voltage):.3f} ,"
	datas += " \"AC_Amp\": "+ f"{float(LS_Current):.3f} ,"
	datas += " \"AC_Watt\": "+f"{float(LS_Power):.3f} ,"
	datas += " \"PS_Temp\": "+f"{float(LP_Temp):.3f} ,"
	datas += " \"DC_Volt\": "+f"{float(LP_Volt):.3f} ,"
	datas += " \"DC_Amp\": "+ f"{float(LP_Amp):.3f} ,"
	datas += " \"DC_Watt\": "+f"{float(LP_Watt):.3f} "

	datas += " }"
	count += 1  # ______________________________________________________ for next send
	if ( R_good ) :
		mqttR.publish(R_topic,datas)
		print("___+",dtsf,"publish",R_topic,"\n",datas)
		reset_analog_values() # ________________________________________ in case next minute no NEW subscribed data come in show -0.007
	else :
		try:
			mqttR.connect(R_broker_ip, R_port) # _______________________ try connect again
			R_good = True
		except:
			print("--- Remote mqtt broker NOT connect again!")


while True:
	nowt = datetime.now()
	dnowt = lastt.minute - nowt.minute

	if(dnowt != 0) : # 1 min timer
		dtsf = nowt.strftime("%Y_%m_%d_%H_%M_%S")
		send_to_remote()
		lastt=nowt

	time.sleep(0.5) # __________________________________________________ with 2 python tools run on RPI see 15% cpu load, now use sleep timer 
	#  _________________________________________________________________ update both mqtt
	mqttR.loop(.1)
	mqttL.loop(.1)
