#!/usr/bin/env python3
# need installed:
# pip3 install paho-mqtt

# revision with using .env file
# pip3 install python-dotenv

# Copyright 2021 HiveMQ GmbH
import paho.mqtt.client as paho
from paho import mqtt
# MOD KLL 2022-12-15

import time
from datetime import datetime
from dotenv import load_dotenv
import os,sys,shutil
encoding = 'utf-8'
import json


load_dotenv()

R_broker_ip=os.getenv('remote_clusterURL')
R_port=int(os.getenv('remote_port') )
R_user=os.getenv('remote_MQTT_user')
R_pwd=os.getenv('remote_MQTT_pass')
R_mtopic=os.getenv('remote_mtopic')
R_topic=R_mtopic+"/#"

startt = datetime.now() # local RPI time

JSONs="{}"


def on_connect(mqttc, obj, flags, rc):
    print("___ connect rc: " + str(rc))

def on_message(mqttc, obj, msg):
    global startt
    nowt = datetime.now()
    dtsf = nowt.strftime("%Y_%m_%d_%H_%M_%S")
    print("___ " + dtsf + " " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("___ published mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("___ subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)

print("___ connect and subscribe to HIVEMQ.com free developer account and wait if BRIDGE send local data")
startt = datetime.now()
print("___ start:",startt)

mqttR = paho.Client(client_id="py_remote_sub", userdata=None, protocol=paho.MQTTv311)
mqttR.username_pw_set(username=R_user,password=R_pwd) # ________________ HIVEMQ credentials
mqttR.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS) # ______________ with account must use TLS and 8883
mqttR.on_message = on_message
mqttR.on_connect = on_connect
mqttR.on_publish = on_publish
mqttR.on_subscribe = on_subscribe
# mqttR.on_log = on_log
mqttR.connect(R_broker_ip, R_port)

mqttR.subscribe((R_topic, 0)) # ________________________________________ get back data from HIVEMQ send by local bridge

#mqttR.loop_forever()

while True :
    mqttR.loop(.1)
    time.sleep(1)

