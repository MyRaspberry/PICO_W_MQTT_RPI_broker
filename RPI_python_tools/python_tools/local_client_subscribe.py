#!/usr/bin/env python3
# need installed:
# pip3 install paho-mqtt

# revision with using .env file
# pip3 install python-dotenv

import paho.mqtt.client as mqtt
import time
from datetime import datetime
from dotenv import load_dotenv
import os,sys,shutil
encoding = 'utf-8'
import json


load_dotenv()
L_broker_ip=os.getenv('MQTT_broker')
L_port=int(os.getenv('MQTT_port') )
L_user=os.getenv('MQTT_user')
L_pwd=os.getenv('MQTT_pass')
L_mtopic=os.getenv('MQTT_mtopic')
L_dtopic=os.getenv('MQTT_dtopic')
L_S31topic=os.getenv('MQTT_S31topic')

L_topic_PICOW=L_mtopic+'/'+L_dtopic
L_topic_S31=L_mtopic+'/'+L_S31topic

startt = datetime.now() # local RPI time UTC

JSONs="{}"


def on_connect(mqttc, obj, flags, rc):
    print("___ connect rc: " + str(rc))

def on_message(mqttc, obj, msg):
    global startt
    nowt = datetime.now()
    dtsf = nowt.strftime("%Y_%m_%d_%H_%M_%S")
    print("___ "+dtsf + " " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("___ published mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)

startt = datetime.now()
print(startt)

mqttL = mqtt.Client("py_local_sub")
mqttL.username_pw_set(username=L_user,password=L_pwd) # ________________ as we use RPI4 Mosquitto2 streamsheets with this connector
mqttL.on_message = on_message
mqttL.on_connect = on_connect
mqttL.on_publish = on_publish
mqttL.on_subscribe = on_subscribe
# mqttL.on_log = on_log
mqttL.connect(L_broker_ip, L_port, 60)
mqttL.subscribe([(L_topic_PICOW, 0),(L_topic_S31, 0)]) # _______________ get data from PICO_W and S31

mqttL.loop_forever()
