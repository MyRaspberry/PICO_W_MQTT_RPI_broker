# called from jobs.py : job2
import os
import time
import board
from jobs import dp

useDHT = False # a linked sensor DHT22 by 'wire' on pin 1 PICO W
useDHT = bool(os.getenv('useDHT'))

def get_useDHT() :
    return useDHT

# need file /lib/adafruit_dht.mpy
# a linked sensor DHT22 by 'wire' on pin 1 PICO W
# might need pullup 10k resistor on data pin / here works without

import adafruit_dht
if ( useDHT ) :
    dht = adafruit_dht.DHT22(board.GP0) # pin 1 'UART0 TX' used with 'wire code'

temperature = 0.0
humidity = 0.0

# to get last reading ( like to webserver ) without new reading
def get_Temp() :
    return temperature

def get_Humid() :
    return humidity

def get_DHT() :
    global temperature, humidity
    try :
        temperature = dht.temperature
        humidity = dht.humidity
        dp("___+ DHT: Temp: {:.1f} degC ".format(temperature))
        dp("___+ DHT: Humidity: {} %".format(humidity))
    except RuntimeError as e:
        print("Reading from DHT failure: ", e.args)

