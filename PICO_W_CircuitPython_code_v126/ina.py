# called from jobs.py : job3
# _______________________________________________________________ INA219 board with filtered values
import os
import time
import board
from jobs import dp

import busio
import board

useINA = False #__________________________________________________ INA219 at 0x40
useINA = bool(os.getenv('useINA'))

def get_useINA() :
    return useINA

I2Cok = False

if ( useINA) :
    try:
        #i2c = busio.I2C(board.SCL1, board.SDA1) # SDA1 pin 6 SCL1 pin7 ( SDA SCL not in board ?? )
        i2c = busio.I2C(board.GP5, board.GP4) # SDA1 pin 6 SCL1 pin7 ( SDA SCL not in board ?? )
        I2Cok = True
    except Exception as e:
        print("Error: INA I2C no pullup, not connected\n", str(e))

    # expect /lib/adafruit_ina219.mpy
    # expect /lib/adafruit_register/...

    from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
else :
    dp("___--- INA disabled")

ina219bus_v=0.0
ina219shunt_v=0.0
ina219amp=0.0
ina219watt=0.0

# for use in MQTT
def get_INA_Volt() :
    return  (ina219bus_v+ina219shunt_v)

def get_INA_Amp() :
    return ina219amp

def get_INA_Watt() :
    return ina219watt


def get_ina219() : # _____ now with filter for reading every second inbetween mqtt sampling
    global  ina219bus_v, ina219shunt_v, ina219amp, ina219watt
    if ( useINA ) :
        ina219bus_v = ina219.bus_voltage  # voltage on V- (load side)
        ina219shunt_v = ina219.shunt_voltage  # voltage between V+ and V- across the shunt
        ina219amp = ina219.current/1000.0  # current in A
        ina219watt = ina219.power  # power in watts
        print_ina219_data()


def print_ina219_data() :
    if ( useINA ) :
        dp("___ {:6.3f} [V], {:6.3f} [A], {:6.3f} [W]".format((ina219bus_v + ina219shunt_v), (ina219amp), (ina219watt) ) )


def print_ina219_detail():
    if ( useINA ) :
        dp("___++INA detail readings:")
        dp("___+ Voltage (VIN+) : {:6.3f}   V".format(ina219bus_v + ina219shunt_v))
        dp("___+ Voltage (VIN-) : {:6.3f}   V".format(ina219bus_v))
        dp("___+ Shunt Voltage  : {:8.5f} V".format(ina219shunt_v))
        dp("___+ Shunt Current  : {:7.4f}  A".format(ina219amp))
        dp("___+ Power Calc.    : {:8.5f} W".format(ina219bus_v * (ina219amp)))
        dp("___+ Power Register : {:6.3f}   W".format(ina219watt))

def get_ina219_config():
    if ( useINA ) :
        dp("___++INA config register:")
        dp("___++ bus_voltage_range:    0x%1X" % ina219.bus_voltage_range) # ______ 0x1 / 32V
        dp("___++ gain:                 0x%1X" % ina219.gain) # ___________________ 0x3 / 320mV
        dp("___++ bus_adc_resolution:   0x%1X" % ina219.bus_adc_resolution) # _____ 0xD / 12bit,  32 samples, 17.02ms
        dp("___++ shunt_adc_resolution: 0x%1X" % ina219.shunt_adc_resolution) # ___ 0xD
        dp("___++ mode:                 0x%1X" % ina219.mode) # ___________________ 0x7 / shunt and bus voltage continuous
        dp("___++ calibate:             0x%1X" % ina219.calibration) # ____________ 0x1000 /
        dp("")


if ( I2Cok & useINA ) :
    try:
        ina219 = INA219(i2c) # start the link
    except Exception as e:
        print("Error: no INA? wrong address?\n", str(e))

    # ___ optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
    # ___ MOD
    ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    # ___ optional : change voltage range to 16V
    #ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

    dp("___++ INA219 ")
    # ___ display some of the advanced field (just to test)
    get_ina219_config()
    get_ina219() # ___ get the measuring values
    print_ina219_detail() # only once at startup

# _______________________________________________________________  INA219 board

