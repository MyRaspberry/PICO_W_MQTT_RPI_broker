# called from jobs.py : job4
import os
import board

from jobs import dp

import busio

useADS = False #__________________________________________________ ADS1115 0x48
useADS = bool(os.getenv('useADS'))

def get_useADS() :
    return useADS

I2Cok = False

if useADS :
    try:
        i2c = busio.I2C(board.GP5, board.GP4) # SDA1 pin 6 SCL1 pin7 ( SDA SCL not in board ?? )
        I2Cok = True
    except Exception as e:
        print("Error: ADS I2C no pullup, not connected\n", str(e))

    import adafruit_ads1x15.ads1115 as ADS #_____________ expect /lib/adafruit_ads1x15/..from bundle
    from adafruit_ads1x15.analog_in import AnalogIn as I2C_AIn
    Ads01,Ads23 = 0.0,0.0

    if ( I2Cok & useADS ): #__________________________________________ see pullup so try measure
        try:
            ads = ADS.ADS1115(i2c) # default (i2c,gain: 1,data_rate: None,mode: Mode.SINGLE ( CONTINUOUS ),address: 0x48 )
            # use 4 channel as 2 differential
            chan01 = I2C_AIn(ads, ADS.P0, ADS.P1 )
            chan23 = I2C_AIn(ads, ADS.P2, ADS.P3 )
            #ads.gain = 1 #2/3,1,2,4,8,16  as 6,4,2,1,0.5,0.25 V
            dp("___++ ADS1115 differential / C1 P0 P1 / C2 P2 P3 /")
            dp("___++ ads gain: %d " % ads.gain)
        except Exception as e:
            print("Error: ADS I2C not connected\n", str(e))
            I2Cok = False # ___ link ok, but device NOT
else:
    dp("___--- ADS disabled")

ADSVolt, ADSAmp, ADSWatt = 0.0, 0.0, 0.0


def get_ADS_Volt():
    return ADSVolt


def get_ADS_Amp():
    return ADSAmp


def get_ADS_Watt():
    return ADSWatt


def get_ADS():
    global ADSVolt, ADSAmp, ADSWatt
    Ads01i, Ads23i =0.0, 0.0
    Ads01v, Ads23v =0.0, 0.0
    a01, f01 = 0.0, 10.0 # Volt range with voltage divider 33V to 3.3V
    a23, f23 = 0.0, 25.0 # Amp range with ACS758 50A to 3.3V
    try:
        if ( I2Cok & useADS ) :
            # use 4 channel as 2 differential
            #chan01 = I2C_AIn(ads, ADS.P0, ADS.P1 )
            #chan23 = I2C_AIn(ads, ADS.P2, ADS.P3 )
            Ads01v = chan01.voltage
            Ads23v = chan23.voltage
            Ads01i = chan01.value
            Ads23i = chan23.value
            dp("___++ ADS1115 chan01 {:>5}\t{:>5.3f} [V]".format(Ads01i, Ads01v))
            dp("___++ ADS1115 chan23 {:>5}\t{:>5.3f} [V]".format(Ads23i, Ads23v))         # ADS I2C code

    except RuntimeError as e:
        print("Reading from ADS failure: ", e.args)

    ADSVolt = a01 + f01 * Ads01v
    ADSAmp  = a23 + f23 * Ads23v

    ADSWatt = ADSVolt * ADSAmp
    dp("___+ ADS: Volt: {:.2f} V".format(ADSVolt))
    dp("___+ ADS: Amps: {:.2f} A".format(ADSAmp))
    dp("___+ ADS: Watt: {:.2f} W".format(ADSWatt))


#
