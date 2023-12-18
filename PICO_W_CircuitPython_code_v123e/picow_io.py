# PICO W with CP
# called from jobs.py : job1
from jobs import dp

import os
import board
import digitalio
import microcontroller # ____________________________________ needed for CPU temperature
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True  # _________________________________________ after boot LED ON helps to see its working.. at a timed job ( here getAins() ) blink
dp("___+++ board LED ON")

DO1set = False
DO1 = digitalio.DigitalInOut(board.GP1)
DO1.switch_to_output(value=True) # __________________________ no boot blink! thanks @deʃhipu
#DO1.direction = digitalio.Direction.OUTPUT
#DO1.value = not DO1set  # __________________________________ after boot DO1 ( ext LED output high ) aka LED OFF BUT IT BLINKS
dp("___+++ DO1 on GP1 HIGH")


Button2 = digitalio.DigitalInOut(board.GP2) # _______________ PB on GP2 wired to GND
Button2.switch_to_input(pull=digitalio.Pull.UP) # ___________ normal 0 pressed 1
dp("___+++ PB2 on GP2, normal 0 pressed 1")
PB2_last = False
PB2_now = False

useMCC = True
useMCC = bool(os.getenv('useMCC'))

from analogio import AnalogIn


# filled by function getAins()
A0val = 0.0
A1val = 0.0
A2val = 0.0
T0val = 0.0

# to get last reading ( like to webserver ) without new reading
def get_A0val() :
    return A0val

def get_A1val() :
    return A1val

def get_A2val() :
    return A2val

def get_T0val() :
    return T0val


def get_volt(pin):
    return (pin.value * 3.3) / 65536


def get_pct(pin):
    return (pin.value * 100.0) / 65536


def getAins():
    analog_in0 = AnalogIn(board.A0)  # GP26 pin 31
    analog_in1 = AnalogIn(board.A1)  # GP27 pin 32
    analog_in2 = AnalogIn(board.A2)  # GP28 pin 34
    global A0val, A1val, A2val,T0val, led
    led.value = False
    A0val = get_volt(analog_in0)
    A1val = get_volt(analog_in1)
    A2val = get_volt(analog_in2)
    analog_in0.deinit()
    analog_in1.deinit()
    analog_in2.deinit()
    T0val = microcontroller.cpu.temperature
    #  print sensor data to the REPL
    #print()
    dp("___+ A0: %.3f [V], A1: %.3f [V], A2: %.3f [V], T0: %.2f [degC] " % (A0val,A1val,A2val,T0val))

    led.value = True

mqttsDIO=""
mqttsDIO_mustSend=0

# read from web_wifi:
def get_mqttsDIO():
    return mqttsDIO

def get_mqttsDIO_mustSend() :
    return mqttsDIO_mustSend


def mqtt_DIO_change(channel=1,chval=False) :
    global mqttsDIO, mqttsDIO_mustSend
    mqttsDIO = "{ \"DIO"
    mqttsDIO += f"{channel}" # GPx
    mqttsDIO += "\": "
    #mqttsDIO += f"{chval}" # python logic True False, JSON logic true false, so Node-Red see a STRING not a object!
    if ( chval ) :
        mqttsDIO += "1"
    else :
        mqttsDIO += "0"
    mqttsDIO += "}"

    mqttsDIO_mustSend += 1 # web+wifi see that increase and send above mqtt


def toggle_DO1() :
    global DO1set
    if ( DO1set ) :
        DO1set = False
    else :
        DO1set = True

    DO1.value = not DO1set  # ___________________________________ inverted set DO1 ( ext LED output )
    dp(f"___+++ DO1 on GP1 {DO1set} from PB2")
    mqtt_DIO_change(1,DO1set) # _________________________________ !! i not see that working ???

def set_DO1(dset=True) :
    global DO1set
    DO1set = dset
    DO1.value = not DO1set  # ___________________________________ inverted set DO1 ( ext LED output )
    dp(f"___+++ DO1 on GP1 {DO1set} from HTTP")
    mqtt_DIO_change(1,DO1set)

def set_DO1_remote(dset=True) :
    global DO1set
    DO1set = dset
    DO1.value = not DO1set  # ___________________________________ inverted set DO1 ( ext LED output ) via MQTT
    dp(f"___+++ DO1 on GP1 {DO1set} from MQTT")
    mqtt_DIO_change(1,DO1set)


def runDIO() : # ________________________________________________ called from jobs
    # get PB2 on GP2
    global PB2_last, PB2_now
    ts=time.monotonic()
    #led.value = False # not see, too short
    #Button2 = digitalio.DigitalInOut(board.GP2) # ______________ PB on GP2 wired to GND
    #Button2.switch_to_input(pull=digitalio.Pull.UP) # __________ normal 0 pressed 1
    PB2_now = Button2.value
    #dp(PB2_now)
    #dp(f"___+ runDIO PB2: {PB2_now} at {ts}")
    if ( PB2_now == False ):
        if ( PB2_last == False ) :
            dp(f"___ still PB2 PRESSED {ts}")
        else :
            if ( useMCC ) :
                toggle_DO1()  # _____________________________________ press "PB2" ON press OFF
            dp(f"___ change to PB2 PRESSED {ts}")
            mqtt_DIO_change(2,True)
    if ( PB2_now == True ):
        if ( PB2_last == False ) :
            dp(f"___ change to PB2 UNPRESSED {ts}")
            mqtt_DIO_change(2,False)

        else :
            pass # dp("___ PB2 still UNPRESSED")
    PB2_last = PB2_now

    #dp("0", "")
    #led.value = True
