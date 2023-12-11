# file: web_wifi.py
# ____________________________________________________ expect file: settings.toml
import os
import time
from adafruit_datetime import  datetime

import micropython
#import gc # micropython garbage collection # use gc.mem_free() # use gc.collect
THIS_REVISION = os.getenv('THIS_REVISION')
THIS_OS = os.getenv('THIS_OS')

WIFI_SSID = os.getenv('WIFI_SSID')
WIFI_PASSWORD = os.getenv('WIFI_PASSWORD')

TZ_OFFSET = os.getenv('TZ_OFFSET') # for NTP to RTC
useNTP = os.getenv('useNTP')

def get_network_time():
    if ( useNTP == 1 ) :
        try:
            print("___ get NTP to RTC")
            ntp = adafruit_ntp.NTP(pool, tz_offset=TZ_OFFSET)
            rtc.RTC().datetime = ntp.datetime # NOTE: This changes the system time
        except:
            print("failed")

def show_time(lDIAG=True):
    if  (useNTP == 1 ) :
        #print(time.localtime())
        tnow = datetime.now()
        tnows = tnow.isoformat()
        tnows = tnows.replace("T"," ")
        if lDIAG:
            dp(tnows)
        return tnows
    else :
        return " "


WIFI_IP = os.getenv('WIFI_IP')

from jobs import dp

import rtc
import adafruit_ntp # V1.2.3 c use NTP time to set PICO W RTC

import socketpool
from ipaddress import ip_address
import wifi

HtmlStyle =   '<style>'
HtmlStyle +=   'html {font-family: "Times New Roman", Times, serif; background-color: lightgreen;'
HtmlStyle +=   'display:inline-block; margin: 0px auto; text-align: center;}'
HtmlStyle +=   'h1{color: deeppink; width: 200; word-wrap: break-word; padding: 2vh; font-size: 35px;}'
HtmlStyle +=   'p{font-size: 1.5rem; width: 200; word-wrap: break-word;}'
HtmlStyle +=   '.button{font-family: {font_family};display: inline-block;'
HtmlStyle +=   'background-color: black; border: none;'
HtmlStyle +=   'border-radius: 4px; color: white; padding: 16px 40px;'
HtmlStyle +=   'text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}'
HtmlStyle +=   'p.dotted {margin: auto; width: 75%; font-size: 25px; text-align: center;}'
HtmlStyle +=   '</style>'

def html_index_page():
    htmldata =  '<!DOCTYPE html><html><head><title>KLL Pico W Web Server</title>'
    htmldata += HtmlStyle
    htmldata += '</head><body>'
    htmldata += '<h1>KLL Pico W Web Server</h1><h2> from Circuit Python'
    htmldata += THIS_OS + '</h2>'
    htmldata += '<img src="https://www.raspberrypi.com/documentation/microcontrollers/images/pico-pinout.svg" >'
    htmldata += '<p> image PICO W </p><hr></br><a href="/data" target="_blank" ><b>data</b></a> <hr>'
    htmldata += '<p>  <a href="http://kll.byethost7.com/kllfusion01/infusions/articles/articles.php?article_id=218" target="_blank" ><b>kll engineering blog</b></a> rev: '
    htmldata += THIS_REVISION
    htmldata += '</p>'
    htmldata += '</body></html>'
    return htmldata

from jobs import get_JOB0en, get_JOB1en, get_JOB2en, get_JOB3en, get_JOB4en

from picow_io import get_A0val, get_A1val, get_A2val, get_T0val, set_DO1, set_DO1_remote, get_mqttsDIO, get_mqttsDIO_mustSend

from dht import get_Temp, get_Humid

from ina import get_INA_Volt, get_INA_Amp, get_INA_Watt

from ads import get_ADS_Volt, get_ADS_Amp, get_ADS_Watt

def html_data_page():
    JOB0en=get_JOB0en()
    JOB1en=get_JOB1en() # readback if operated
    JOB2en=get_JOB2en()
    JOB3en=get_JOB3en()
    JOB4en=get_JOB4en()

    if JOB1en :
        pass

    if JOB1en :
        #get A0val,A1val,A2val from picow_io.py last get_Ains() reading via getAxval() functions
        A0vals = ' %.4f ' % get_A0val()
        A1vals = ' %.4f ' % get_A1val()
        A2vals = ' %.4f ' % get_A2val()
        T0vals = ' %.1f ' % get_T0val()

    if JOB2en :
        # get temperature, humidity from dht.py last get_DHT() reading via get_Temp() get_Humid() functions
        Temps = ' %.2f ' % get_Temp()
        Humids  = ' %.2f ' % get_Humid()

    if JOB3en :
        INA_Volts = ' %.2f ' % get_INA_Volt()
        INA_Amps = ' %.2f ' % get_INA_Amp()
        INA_Watts = ' %.2f ' % get_INA_Watt()

    if JOB4en :
        ADS_Volts = ' %.2f ' % get_ADS_Volt()
        ADS_Amps = ' %.2f ' % get_ADS_Amp()
        ADS_Watts = ' %.2f ' % get_ADS_Watt()


    htmldata =   '<!DOCTYPE html><html><head><title>KLL Pico W Web Server DATA</title><meta http-equiv="refresh" content="15">'

    htmldata +=   HtmlStyle

    htmldata +='</head><body><div> <p> <h1> PICO W : DATA from JOBS </h1> </p> <hr>'
    if JOB0en :
        htmldata +=  ' <p> <b> PICO W drive Digital out </b> to LED  </h2>'
        htmldata +=  '<form accept-charset="utf-8" method="POST">'
        htmldata +=  '<button class="button" name="LED ON" value="ON" type="submit">DO1 LED ON</button></a></p></form>'
        htmldata +=  '<p><form accept-charset="utf-8" method="POST">'
        htmldata +=  '<button class="button" name="LED OFF" value="OFF" type="submit">DO1 LED OFF</button></a></p></form>'
    else:
        htmldata +=  '<p>Dout currently not enabled</p>'

    if JOB1en :
        htmldata +=  ' <p> <b> PICO W measure Analog In </b> in [V]  </p>'
        htmldata +=  ' <table style="border:solid" ><tr><th style="border:solid">A0</th>'
        htmldata +=  '<th style="border:solid" >A1</th><th style="border:solid">A2</th>'
        htmldata +=  '<th style="border:solid">T0</th></tr>'
        htmldata += f' <tr><td style="border:solid">{A0vals} V</td><td style="border:solid">{A1vals} V</td>'
        htmldata += f'<td style="border:solid">{A2vals} V</td><td style="border:solid">{T0vals} C</td></tr></table>'
    else :
        htmldata += '<p>AIN currently not enabled</p>'

    if JOB2en :
        htmldata +=  '<p> <b> PICO W measure via wire link DHT22 sensor breakout :</b> </p>'
        htmldata +=  '<table style="border:solid" ><tr><th style="border:solid">Temp</th><th style="border:solid" >Humid</th></tr>'
        htmldata += f' <tr><td style="border:solid">{Temps} degC</td><td style="border:solid">{Humids} %</td></tr></table>'
    else :
        htmldata += '<p>DHT currently not enabled</p>'

    if JOB3en :
        htmldata +=  '<p> <b> PICO W measure via I2C link INA219 sensor breakout :</b> </p>'
        htmldata +=  '<table style="border:solid" ><tr><th style="border:solid">Volt</th><th style="border:solid" >Amp</th><th style="border:solid" >Watt</th></tr>'
        htmldata += f' <tr><td style="border:solid">{INA_Volts} V</td><td style="border:solid">{INA_Amps} A</td><td style="border:solid">{INA_Watts} W</td></tr></table>'
    else :
        htmldata += '<p>INA currently not enabled</p>'

    if JOB4en :
        htmldata +=  '<p> <b> PICO W measure via I2C link ADS1115 sensor breakout as 2 differential channels:</b> </p>'
        htmldata +=  '<table style="border:solid" ><tr><th style="border:solid">Volt</th><th style="border:solid" >Amp</th><th style="border:solid" >calc Watt</th></tr>'
        htmldata += f' <tr><td style="border:solid">{ADS_Volts} V</td><td style="border:solid">{ADS_Amps} A</td><td style="border:solid">{ADS_Watts} W</td></tr></table>'
    else :
        htmldata += '<p>ADS currently not enabled</p>'

    htmldata +=  '<hr><h2>'
    htmldata +=  show_time(False)
    htmldata +=  '</h2><p>( page autorefresh 15s)</p> '
    #htmldata +=  '<b>return adafruit_httpserver.HTTPResponse(content_type=adafruit_httpserver.MIMEType._MIME_TYPES["html"], body=html_data_page() ) </b></br>'
    #htmldata +=  'thanks to Circuit Python forum: "anecdata"</p>'
    htmldata +=  '</div>'
    htmldata +=  '</body></html>'
    #nohtmldata = f'measure Analog In ( every 30 sec ):  A0: {A0val} A1: {A1val} A2: {A2val} in [V] ( no autorefresh )'
    return htmldata

dtsleep = 0

# OLD ____________________________________________________ expect /lib/adafruit_httpserver.mpy
# OLD ____________________________________________________ ( copy from adafruit-circuitpython-bundle-8.x-mpy-20221104.zip ! old CP800b4 ! to PICO W )
# OLD import  adafruit_httpserver
# ____________________________________________________ expect /lib/adafruit_httpserver/*
# ____________________________________________________ ( copy from adafruit-circuitpython-bundle-8.x-mpy-20221209.zip ! upgrade CP800b5 ! to PICO W )
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType

from mqtt import get_useMQTT, get_mqtts, get_MQTT_count, get_useFilter_Tuning, set_useFilter, set_filter_Va, set_filter_Ia, set_filter_Wa # check if we need MQTT inhere ( files: job5 mqtt )
from jobs import set_update5

MQTT_count = 0 # local but get from mqtt.py

def mqtt_connect() :
    global server, mqtt_client, mqtt_topic, MQTTok, pool, use_REMOTE_broker
    if ( get_useMQTT() ) :
        dp("___+++ setup MQTT")
        import adafruit_minimqtt.adafruit_minimqtt as MQTT
        import json
        import ssl

        MQTTok = False
        MQTT_broker = os.getenv('MQTT_broker') # ___ RPI IP
        MQTT_port = os.getenv('MQTT_port') # __ 1883
        MQTT_user = os.getenv('MQTT_user') # _______ u213
        MQTT_pass = os.getenv('MQTT_pass') # _______ p213
        MQTT_TLS = os.getenv('MQTT_TLS') # _________ "n"
        MQTT_mtopic = os.getenv('MQTT_mtopic')
        MQTT_dtopic = os.getenv('MQTT_dtopic')

        use_REMOTE_broker = os.getenv('use_REMOTE_broker')
        if ( use_REMOTE_broker == "y" ):
            MQTT_broker = os.getenv('remote_broker') # ___ HIVEMQ
            MQTT_port = os.getenv('remote_port') # __ 8883
            MQTT_user = os.getenv('remote_user') # _______
            MQTT_pass = os.getenv('remote_pass') # _______
            MQTT_TLS = os.getenv('remote_TLS') # _________ "y"

            MQTT_mtopic = os.getenv('remote_mtopic') # THIS data scheme
            MQTT_dtopic = os.getenv('remote_dtopic') # THIS SITE

        MQTT_count = 0 # _____________________________________ send to broker as id too
        mqtt_hello="Hello Broker: i am a PICO W"
        mqtt_topic = MQTT_mtopic + "/" + MQTT_dtopic # like DC power supply measurements Volt Amp Watt DC as JSON
        ### MQTT Code ###
        # Define callback methods which are called when events occur
        # pylint: disable=unused-argument, redefined-outer-name
        def connect(mqtt_client, userdata, flags, rc):
            # This function will be called when the mqtt_client is connected
            # successfully to the broker.
            dp("___ Connected to MQTT Broker!")
            dp("___ Flags: {0} RC: {1}".format(flags, rc))


        def disconnect(mqtt_client, userdata, rc):
            # This method is called when the mqtt_client disconnects
            # from the broker.
            dp("___ Disconnected from MQTT Broker!")


        def subscribe(mqtt_client, userdata, topic, granted_qos):
            # This method is called when the mqtt_client subscribes to a new feed.
            dp("___ Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


        def unsubscribe(mqtt_client, userdata, topic, pid):
            # This method is called when the mqtt_client unsubscribes from a feed.
            dp("___ Unsubscribed from {0} with PID {1}".format(topic, pid))


        def publish(mqtt_client, userdata, topic, pid):
            # This method is called when the mqtt_client publishes data to a feed.
            dp("___ Published to {0} with PID {1} ".format(topic, pid))


        def message(client, topic, message):
            #global Va,Vb,Aa,Ab,Wa,Wb # here overwritten
            # Method called when a client's subscribed feed has a new value.
            dp("___ New message on topic {0}: {1}".format(topic, message))
            if ( get_useFilter_Tuning() ) : # in mqtt.py allow if remote tuning possible
                setJson = json.loads(message)
                #print(setJson)
                if ( 'Vtune' in message  ) :
                    Va = setJson['Vtune']
                    Vb = 1.0-Va
                    set_filter_Va(Va) # set it in mqtt.py
                    dp("___ set V filter tune Va {0}, Vb {1}".format(Va,Vb) )
                if ( 'Atune' in message  ) :
                    Aa = setJson['Atune']
                    Ab = 1.0-Aa
                    set_filter_Ia(Aa) # set it in mqtt.py
                    dp("___ set A filter tune Aa {0}, Ab {1}".format(Aa,Ab) )
                if ( 'Wtune' in message  ) :
                    Wa = setJson['Wtune']
                    Wb = 1.0-Wa
                    set_filter_Wa(Wa) # set it in mqtt.py
                    dp("___ set W filter tune Wa {0}, Wb {1}".format(Wa,Wb) )
                if ( 'ttune' in message  ) :
                    mqttrate = setJson['ttune']
                    set_update5(mqttrate)
                    dp("___ set MQTTrate {0}".format(mqttrate) )
                if ( 'useFilter' in message ):
                    use = setJson['useFilter'] # expect 0 or 1 number for boolen?
                    set_useFilter(use) # set it in mqtt.py
                    dp("___ set useFilter {0}".format(use) )
                # 1.1.3.b4 DIO mqtt set
                if ( 'DO1' in message ):
                    DO1set = setJson['DO1'] # expect 0 or 1 number for boolen?
                    set_DO1_remote(DO1set) # set it in picow_io
                    dp("___ set DO1 {0}".format(DO1set) )

        ### END MQTT functions ###


        # Set up a MiniMQTT Client !! from adafruit example NOT use client name?
        # https://docs.circuitpython.org/projects/minimqtt/en/latest/api.html
        # client_id (str) – Optional client identifier, defaults to a unique, generated string.
        dp("___+++ setup MQTTclient")
        if ( MQTT_TLS == "y" ) :
            dp("___++++ use TLS")
            mqtt_client = MQTT.MQTT(
                broker=MQTT_broker,
                port=MQTT_port,
                username=MQTT_user,
                password=MQTT_pass,
                socket_pool=pool,
                ssl_context=ssl.create_default_context()
            )
        else :
            dp("___++++ NO TLS")
            mqtt_client = MQTT.MQTT(
                broker=MQTT_broker,
                port=MQTT_port,
                username=MQTT_user,
                password=MQTT_pass,
                socket_pool=pool
                #ssl_context=ssl.create_default_context(),
            )

        # Connect callback handlers to mqtt_client
        mqtt_client.on_connect = connect
        mqtt_client.on_disconnect = disconnect
        mqtt_client.on_subscribe = subscribe
        mqtt_client.on_unsubscribe = unsubscribe
        mqtt_client.on_publish = publish
        mqtt_client.on_message = message

        try:
            dp("___ Attempting to connect to %s" % mqtt_client.broker)
            mqtt_client.connect()
            MQTTok = True # _______________________________ used later for publish
        except Exception as e:
            print("Error: MQTT connect\n", str(e))
            MQTTok = False

        try:
            dp("___ Publishing to %s" % MQTT_mtopic) # ____ only master topic gets that
            dp(mqtt_hello)
            mqtt_client.publish(MQTT_mtopic,mqtt_hello )
            MQTTok = True # _______________________________ used later for publish
        except Exception as e:
            print("Error: MQTT publish hello\n", str(e))
            #MQTTok = False

        try:
            # setup subscribe
            mqtt_topic_tune = mqtt_topic + "/set"
            dp("___ Subscribing to %s tuning" % mqtt_topic_tune)
            mqtt_client.subscribe(mqtt_topic_tune)
        except Exception as e:
            print("Error: MQTT subscribe tuning\n", str(e))
            #MQTTok = False

        dp("___ MQTT broker: "+MQTT_broker)
        dp("___ mqtt_topic: "+mqtt_topic)


def setup_webserver() :
    global server, mqtt_client, mqtt_topic, MQTTok, pool
    dp("\n\n___ PICO W: Hello World! start webserver (STA)\n")
    dp("___ Connecting to router {:s} OR CHECK THE 'settings.toml' FILE".format( WIFI_SSID) )
    wifi.radio.set_ipv4_address( # _______________________ fixIP ( requires > CP 8.0.0 beta 4 )
        ipv4=ip_address(WIFI_IP),
        netmask=ip_address("255.0.0.0"),
        gateway=ip_address("192.168.1.1"),
        ipv4_dns=ip_address("192.168.1.1"),
    )
    wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
    dp("___ Connected to {:s}".format( WIFI_SSID) )
    dp("___ Listening on http://{:s}:80 ".format(str(wifi.radio.ipv4_address)) )

    pool = socketpool.SocketPool(wifi.radio)

    # get network time to RTC
    get_network_time()
    show_time()

    # make a WEB SERVER
    server = HTTPServer(pool)

    @server.route("/")
    def base(request):  # pylint: disable=unused-argument
        dp("\nwifi served dynamic index.html")
        #return HTTPResponse(content_type=MIMEType.TYPE_HTML, body=html_index_page() )
        response = HTTPResponse(request)
        with response:
            response.send(body=html_index_page(), content_type=MIMEType.TYPE_HTML)

    @server.route("/data")
    def data(request):  # pylint: disable=unused-argument
        dp("\nwifi served dynamic data.html")
        #return HTTPResponse(content_type=MIMEType.TYPE_HTML, body=html_data_page() )
        response = HTTPResponse(request)
        with response:
            response.send(body=html_data_page(), content_type=MIMEType.TYPE_HTML)

    #  if a button is pressed on the site
    @server.route("/data", method=HTTPMethod.POST)
    def buttonpress(request: HTTPRequest):
        raw_text = request.raw_request.decode("utf8") #  get the raw text
        dp(raw_text)

        if "ON" in raw_text: #  if the led on button was pressed
            #  turn on the onboard LED
            set_DO1(True)

        if "OFF" in raw_text: #  if the led off button was pressed
            #  turn the onboard LED off
            set_DO1(False)

        #  reload site
        response = HTTPResponse(request)
        with response:
            response.send(body=html_data_page(), content_type=MIMEType.TYPE_HTML)


    server.start(str(wifi.radio.ipv4_address)) # _________ startup the server

    mqtt_connect() # ______________________________________ above MQTT start


mqttsDIO_mustSend=0 # but read from picow_io

def mqtt_DIO_change_send() : # _________________________________ can be Din report or Dout change back report
    global MQTTok, mqttsDIO_mustSend
    mustSend=False
    # data from picow_io
    mqttsDIO = get_mqttsDIO()
    mqttsDIO_mustSend_check = get_mqttsDIO_mustSend()
    #dp(f"mqtt_DIO_change_send {mqttsDIO} {mqttsDIO_mustSend_check} ")
    if ( mqttsDIO_mustSend_check > mqttsDIO_mustSend ) : # ___ new DIO stat report from picow_io
        mqttsDIO_mustSend = mqttsDIO_mustSend_check # ______________ remember in global
        mustSend = True
        #dp("new DIO change report")

    if ( get_useMQTT() and MQTTok and mustSend ) :
        mqtt_topic_stat= mqtt_topic + "/stat"
        try: # ____________________________________ but broker can be down now
            mqtt_client.publish(mqtt_topic_stat, mqttsDIO )
            dp(f"___+ DIO_change send to {mqtt_topic_stat} for {mqttsDIO} ")
        except Exception as e:
            print("Error publish DIO:\n", str(e))
            MQTTok = False


mqtt_retry_t = time.monotonic()
mqtt_retry = 10.0 # seconds at start but grows...

def run_webserver() :
    global server, mqtt_client, MQTT_count, mqtt_topic, MQTTok, mqtt_retry_t, mqtt_retry
    try:
        server.poll()
    except OSError:
        print("ERROR server poll")

    # check MQTT
    if ( get_useMQTT() ) :
        if ( MQTTok == False ) :
            nowfailcheck = time.monotonic()
            if ( nowfailcheck >= ( mqtt_retry_t + mqtt_retry ) ) :
                print("RESTART MQTT connection at sec: ", nowfailcheck )
                mqtt_connect()
                mqtt_retry_t = nowfailcheck
                mqtt_retry += 10.0 # next time wait 10 sec longer to check again

    if ( get_useMQTT() and MQTTok) :
        try:
            mqtt_client.loop() # __________________________ now we see the subscribed tuning come through
        except Exception as e:
            print("Error: MQTT loop\n", str(e))
            MQTTok = False
            #time.sleep(60) # ______________________ broker reboot expected
            #microcontroller.reset() # _____________ try reboot case broker recovered

        # check if we have to publish something
        MQTT_new = get_MQTT_count()
        if ( MQTT_new > MQTT_count ) : # ______________ starts at boot, counts up directly after send ( so here is miss the first? )
            MQTT_count = MQTT_new
            mqtts = get_mqtts() # _____________________ get the new record ( as string ) to send from mqtt.py
            #dp("wifi mqtt should send new record")
            try: # ____________________________________ but broker can be down now
                mqtt_client.publish(mqtt_topic, mqtts )
            except Exception as e:
                print("Error publish:\n", str(e))
                MQTTok = False
                #print("Resetting microcontroller in 60 seconds")
                #time.sleep(60) # ______________________ broker reboot expected
                #microcontroller.reset() # _____________ try reboot case broker recovered

    mqtt_DIO_change_send() # ___________________________ only on change by picow_io

