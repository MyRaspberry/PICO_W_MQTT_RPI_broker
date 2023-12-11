# file:  mqtt.py called from jobs.py : job5
# v1.1.1b change filter and decimales
# v1.2.3 c add NTC TRC timestamp to MQTT

import os
import time
from adafruit_datetime import  datetime

from jobs import dp

# we not measure here, we get our data from a other running job
# we not send MQTT here, just make the string for mqtt.payload

useMQTT = False  # ___________________________ used by web_wifi to setup MQTT broker connection
useMQTT = bool(os.getenv('useMQTT'))

MQTTok = False # ____________________________ we dont know from here

MTemp = 0.0
MVolt = 0.0
MAmp = 0.0
MWatt = 0.0

MQTT_dtopic = os.getenv('MQTT_dtopic') # ________________ from settings.toml
MQTT_count = 0
MQTT_counts = '%d' % MQTT_count
#MQTT_count += 1 # for next loop
mqtts = "" # ________________________________ that string will be send

# INA: if useINA and JOB3en True we can get data from ina
from ina import get_useINA, get_INA_Volt, get_INA_Amp, get_INA_Watt
hereuse_INA = False
hereuse_INA = bool(os.getenv('hereuse_INA'))

if ( hereuse_INA and useMQTT ) :
    dp("___+++ MQTT use INA job data")

# normal analog io PICO_W pins
from picow_io import get_A0val, get_A1val, get_T0val
hereuse_PICOW_io = True
hereuse_PICOW_io = bool(os.getenv('hereuse_PICOW_io'))

if (hereuse_PICOW_io and useMQTT ) :
    dp("___+++ MQTT use PICOW IO job data")


def get_useMQTT(): # ________________________ web_wifi use it to setup MQTT
    return useMQTT

# info from: https://learn.adafruit.com/mqtt-in-circuitpython/connecting-to-a-mqtt-broker

# expect /lib/adafruit_minimqtt/
# expect /lib/adafruit_register/

# http://kll.engineering-news.org/kllfusion01/articles.php?article_id=212

if useMQTT:
    try:
        dp("___+++ MQTT setup is done in web_wifi, check this startup")
        #MQTTok = true
    except Exception as e:
        print("Error: MQTT not connected\n", str(e))
else:
    dp("___--- MQTT disabled")


useNTP = os.getenv('useNTP') # send timestamp

useFilter = True
useFilter = bool(os.getenv('useFilter'))
useFilter_Tuning = True

Va = 0.05 # _____________________ FILTER TUNING aka allow 80% change by newly read value only
Vb = 1.0 - Va
Ia = 0.05
Ib = 1.0 - Ia
Wa = 0.05
Wb = 1.0-Wa

def get_useFilter_Tuning() : # ___ web_wifi need it to allow MQTT remote tuning
    return useFilter_Tuning

def set_useFilter(use = True) : # ___ used from web_wifi for MQTT remote tune filter
    global useFilter
    useFilter = use

def set_filter_Va(Vanu = 0.8) : # ___ used from web_wifi for MQTT remote tune filter
    global Va, Vb
    Va = Vanu
    Vb = 1.0 - Va

def set_filter_Ia(Ianu = 0.8) : # ___ used from web_wifi for MQTT remote tune filter
    global Ia, Ib
    Ia = Ianu
    Ib = 1.0 - Ia

def set_filter_Wa(Wanu = 0.8) : # ___ used from web_wifi for MQTT remote tune filter
    global Wa, Wb
    Wa = Wanu
    Wb = 1.0 - Wa


MVoltf,MAmpf,MWattf = 0.0,0.0,0.0
firstrun  = True

use_REMOTE_broker = os.getenv('use_REMOTE_broker')


def send_MQTT(): # ___________________________ called by JOB5 if JOB5en
    global MQTT_count, mqtts, MTemp, MVolt, MAmp, MWatt, MVoltf, MAmpf, MWattf, firstrun
    if  (useNTP == 1 ) :
        #dp("make a timestamp for mqtt record")
        tnow = datetime.now()
        tnows = tnow.isoformat()
        tnows = tnows.replace("T"," ")
        #dp(tnows)
    else:
        tnows = ""


    if (hereuse_PICOW_io ) :
        # if job1 not run should still get 0 ( or old data )
        MTemp = get_T0val() # _________________ PICO W CPU Temp
        # signal in Volt 3v3
        Vmf = 1.0 # ___________________________ tune if use voltage divider
        MVolt = get_A0val() * Vmf
        Amf = 1.0 # ___________________________ tune if use shunt
        MAmp = get_A1val() * Amf
        MWatt = MVolt * MAmp

    if ( hereuse_INA) :
        MTemp = get_T0val() # _________________ PICO W CPU Temp update only if JOB1 run
        # if job3 not run should still get 0 ( or old data )
        MVolt = get_INA_Volt()
        MAmp = get_INA_Amp()
        MWatt = get_INA_Watt()

    if ( useMQTT ) :

        #dp(f"___+++ try mqtt publish : T {MTemp} V {MVolt} A {MAmp} W {MWatt} from INA {hereuse_INA} or PICOW_io {hereuse_PICOW_io} ")
        MTemps = '%.2f' % MTemp
        MVolts = '%.3f' % MVolt
        MAmps = '%.3f' % MAmp
        MWatts = '%.3f' % MWatt
        if ( useFilter ) :
            if ( firstrun ) : # ____________________________________ better filter init
                MVoltf  = MVolt
                MAmpf   = MAmp
                MWattf  = MWatt
                firstrun = False
            else :
                MVoltf  = Va * MVoltf  + Vb * MVolt
                MAmpf   = Ia * MAmpf   + Ib * MAmp
                MWattf  = Wa * MWattf  + Wb * MWatt
                #dp("___++ filter running")

            MVolts = '%.3f' % MVoltf
            MAmps = '%.3f' % MAmpf
            MWatts = '%.3f' % MWattf

        MQTT_counts = '%d' % MQTT_count
        MQTT_count += 1 # for next loop

        if ( use_REMOTE_broker == "y" ): # __________________________ IF talk remote broker same like python BRIDGE
            mqtts = "{" # ___________________________________________ here construct a MQTT JSON like string from the data
            mqtts += " \"id\": "+MQTT_counts
            #mqtts +=", \"dev\":\""+MQTT_dtopic+"\""
            # _______________________________________________________ PICO_W not has realtime now
            mqtts += ", \"minute\": 0"
            mqtts += ", \"datetime\": 0" # replace by broker
            mqtts += ", \"datetimes\": \""+tnows+"\"" # new NTP local time
            # _______________________________________________________ PICO_W not has S31  data
            mqtts += ", \"AC_Volt\": 0.0"
            mqtts += ", \"AC_Amp\": 0.0"
            mqtts += ", \"AC_Watt\": 0.0"

            mqtts +=", \"PS_Temp\": "+MTemps
            mqtts +=", \"DC_Volt\": "+MVolts
            mqtts +=", \"DC_Amp\": "+MAmps
            mqtts +=", \"DC_Watt\": "+MWatts
            mqtts +=" } "
        else:
            mqtts = "{" # ___________________________________________ here construct a MQTT JSON like string from the data
            mqtts += " \"id\": "+MQTT_counts
            mqtts +=", \"dev\":\""+MQTT_dtopic+"\""
            mqtts +=", \"datetimes\": \""+tnows+"\""  # NTP time from V123c

            mqtts +=", \"PS_Temp\": "+MTemps
            mqtts +=", \"DC_Volt\": "+MVolts
            mqtts +=", \"DC_Amp\": "+MAmps
            mqtts +=", \"DC_Watt\": "+MWatts
            mqtts +=" } "

        dp(" rec {:} filtered: {:} Va {:}, Vb {:}, Ia {:}, Ib {:}, Wa {:}, Wb {:}".format ( mqtts, useFilter, Va, Vb, Ia, Ib, Wa, Wb) )

def get_mqtts() :
    return mqtts

def get_MQTT_count() :
    return MQTT_count

# LOG 2022 12 11 ( add CPU Temp )
# JOB5 MQTT make json every 60 sec
# rec { 'id': 0, 'dev':'P01', 'Temp': 37.44, 'Volt': 0.71, 'Amp': 0.73, 'Watt': 0.52 }  filtered: True Va 0.8, Vb 0.2, Ia 0.8, Ib 0.2, Wa 0.8, Wb 0.2
# ___ Published to P213/P01 with PID 1
#1.1.2b2
# rec { "id": 0, "dev":"P01", "Temp": 28.07, "DC_Volt": 0.032, "DC_Amp": -0.000, "DC_Watt": 0.000 }  filtered: True Va 0.1, Vb 0.9, Ia 0.1, Ib 0.9, Wa 0.1, Wb 0.9
#1.1.3b4
# rec { "id": 0, "dev":"Site1/P213", "PS_Temp": 28.54, "DC_Volt": 2.091, "DC_Amp": 0.623, "DC_Watt": 1.303 }  filtered: True Va 0.05, Vb 0.95, Ia 0.05, Ib 0.95, Wa 0.05, Wb 0.95
