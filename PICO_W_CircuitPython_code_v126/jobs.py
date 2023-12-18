# replace all jobx.py with this
# file: jobs.py

import supervisor # ____________________________________ make a serial ( REPL ) input menu to en/dis/able the JOBs ( bad blocking style!! )
import os

# ______________________________________________________ expect a file picow_io.py
usePICOW = True #False # _______________________________ only JOB1 getAins uses PICO W specifics see picow_io.py
usePICOW = bool(os.getenv('usePICOW'))


DIAG = True # False # ___________________________________ global print disable switch / overwritten by console [D][enter]
DIAG = bool(os.getenv('DIAG')) # ______________________________ now get from settings.toml

def dp(line=" ", ende="\n"):
    if DIAG : print(line, end=ende)

if ( usePICOW ) :
    from picow_io import  getAins
    from picow_io import runDIO

JOB0en = True # ________________________________________ enable disable this ONE SEC JOB
JOB0en = bool(os.getenv('JOB0en')) # ___________________ get from setttings.toml
update0 = 0.5 #1
update0 = float(os.getenv('update0'))

def JOB0(): # __________________________________________ basic 0.5 sec job
    #dp("JOB0: every sec")
    if ( usePICOW ) : runDIO() # _______________________ file: picow_io.py

JOB1en = True # ________________________________________ enable disable this JOB
JOB1en = bool(os.getenv('JOB1en')) # ___________________ get from setttings.toml
update1 = 15
update1 = os.getenv('update1')

# called by main timer
def JOB1() : # _________________________________________ THE USER PROGRAM 1 ( <<< here write your code ) NOT MAKE IN HERE BLOCKING CODE AGAIN
    dp("\nJOB1 PICO W board Ains")
    if ( usePICOW ) : getAins()  # _____________________ file: picow_io.py, read/print PICOW A0 A1 A2 and blink LED

# ______________________________________________________ expect a file dht.py
from dht import  get_useDHT, get_DHT
useDHT = False # a linked sensor DHT22 by 'wire' on pin 1 PICO W
useDHT = get_useDHT() # from settings.toml to dht to jobs

JOB2en = False # ________________________________________ enable disable this JOB
JOB2en = bool(os.getenv('JOB2en')) # ___________________ get from setttings.toml
update2 = 12
update2 = os.getenv('update2')

def JOB2() : # _________________________________________ THE USER PROGRAM 2 ( <<< here write your code ) NOT MAKE IN HERE BLOCKING CODE AGAIN
    dp("\nJOB2 linked DHT22")
    if (useDHT) :
        get_DHT()

from ina import get_ina219

JOB3en = False# _________________________________________________ enable disable this JOB
JOB3en = bool(os.getenv('JOB3en')) # ___________________ get from setttings.toml
update3 = 30
update3 = os.getenv('update3')

def JOB3() : # _________________________________________ THE USER PROGRAM 2 ( <<< here write your code ) NOT MAKE IN HERE BLOCKING CODE AGAIN
    dp("\nJOB3 linked INA")
    get_ina219()

from ads import get_ADS
JOB4en = False # ________________________________________ enable disable this JOB
JOB4en = bool(os.getenv('JOB4en')) # ___________________ get from setttings.toml
update4 = 15
update4 = os.getenv('update4')


def JOB4() : # _________________________________________ THE USER PROGRAM 4 ( <<< here write your code ) NOT MAKE IN HERE BLOCKING CODE AGAIN
    dp("\nJOB4 linked ADS")
    get_ADS()

from mqtt import send_MQTT
JOB5en = True # ________________________________________ enable disable this JOB
JOB5en = bool(os.getenv('JOB5en')) # ___________________ get from setttings.toml
update5 = 60
update5 = os.getenv('update5')

def JOB5() : # _________________________________________ THE USER PROGRAM 5 ( <<< here write your code ) NOT MAKE IN HERE BLOCKING CODE AGAIN
    dp("\nJOB5 MQTT make json every {:d} sec".format(update5) )
    send_MQTT()

def get_jupdate5() :
    return update5

def set_update5(update5nu=60) : # for mqtt remote write access
    global update5
    update5 = update5nu

JOB6en = False # _______________________________________ enable disable this JOB
JOB6en = bool(os.getenv('JOB6en')) # ___________________ get from setttings.toml
update6 = 33
update6 = os.getenv('update6')

def JOB6() : # _________________________________________ THE USER PROGRAM 5 ( <<< here write your code ) NOT MAKE IN HERE BLOCKING CODE AGAIN
    dp("\nJOB6 USER SPARE")


# but after we overwrite them here by operator action in USB MENU function console() need to update them from here
def get_JOB0en() :
    return JOB0en

def get_JOB1en() :
    return JOB1en

def get_JOB2en() :
    return JOB2en

def get_JOB3en() :
    return JOB3en

def get_JOB4en() :
    return JOB4en

def get_JOB5en() :
    return JOB5en

def get_JOB6en() :
    return JOB6en

def get_DIAG() :
    return DIAG
# this is if we ever tune job timer ( by menu )
def get_update0() :
    return update0

def get_update1() :
    return update1

def get_update2() :
    return update2

def get_update3() :
    return update3

def get_update4() :
    return update4

def get_update5() :
    update5 = get_jupdate5() # from jobs
    return update5

def get_update6() :
    return update6


from ina import get_useINA

from ads import get_useADS

from mqtt import get_useMQTT

def print_menu() :
    global JOB0en, JOB1en, JOB2en, JOB3en, JOB4en, JOB5en, JOB6en, DIAG
    global update0, update1, update2, update3, update4, update5, update6
    update5 = get_jupdate5() # from jobs
    dp("_________________________________________")
    dp("|  USB MENU PICO W              | timer |")
    dp("|_______________________________|_______|")
    dp("| 0 toggle JOB0  PICOW-DIO   {:b} {:b}| {:0>4} s|".format(JOB0en, usePICOW, update0))
    dp("| 1 toggle JOB1  PICOW-Ains  {:b} {:b}| {:0>4} s|".format(JOB1en, usePICOW, update1))
    dp("| 2 toggle JOB2  DHT22       {:b} {:b}| {:0>4} s|".format(JOB2en, get_useDHT(), update2))
    dp("| 3 toggle JOB3  INA219      {:b} {:b}| {:0>4} s|".format(JOB3en, get_useINA(), update3 ))
    dp("| 4 toggle JOB4  ADS1115     {:b} {:b}| {:0>4} s|".format(JOB4en, get_useADS(), update4 ))
    dp("| 5 toggle JOB5  MQTT send   {:b} {:b}| {:0>4} s|".format(JOB5en, get_useMQTT(), update5 ))
    dp("| 6 toggle JOB6  User Spare  {:b}  | {:0>4} s|".format(JOB6en, update6))
    dp("|                               |       |")
    dp("| d print disable               |       |")
    dp("|_______________________________|_______|")
    dp("| or [m] or [?] for menu        |       |")
    dp("| use [ENTER] to end input      |       |")
    dp("| and prevent blocking          |       |")
    dp("|_______________________________|_______|")

def console() :
    global JOB0en, JOB1en,JOB2en, JOB3en, JOB4en, JOB5en, JOB6en, DIAG
    # better check https://github.com/s-light/CircuitPython_nonblocking_serialinput
    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        # Sometimes Windows sends an extra (or missing) newline - ignore them
        if ( value == "" ) :
            dp("+++ use [?] or [m] for menu")
        if ( value == "?" or value == "m" ) :
            print_menu()
        elif ( value == "0"):
            if JOB0en :
                JOB0en = False
            else:
                JOB0en = True
            dp(">>> JOB0en {}".format( JOB0en ) )
        elif ( value == "1"):
            if JOB1en :
                JOB1en = False
            else:
                JOB1en = True
            dp(">>> JOB1en {}".format( JOB1en ) )
        elif ( value == "2"):
            if JOB2en :
                JOB2en = False
            else:
                JOB2en = True
            dp(">>> JOB2en {}".format( JOB2en ) )
        elif ( value == "3"):
            if JOB3en :
                JOB3en = False
            else:
                JOB3en = True
            dp(">>> JOB3en {}".format( JOB3en ) )
        elif ( value == "4"):
            if JOB4en :
                JOB4en = False
            else:
                JOB4en = True
            dp(">>> JOB4en {}".format( JOB4en ) )
        elif ( value == "5"):
            if JOB5en :
                JOB5en = False
            else:
                JOB5en = True
            dp(">>> JOB5en {}".format( JOB5en ) )
        elif ( value == "6"):
            if JOB6en :
                JOB6en = False
            else:
                JOB6en = True
            dp(">>> JOB6en {}".format( JOB6en ) )


        elif ( value == "d"):
            if DIAG :
                DIAG = False
            else:
                DIAG = True
            dp(">>> DIAG {}".format( DIAG ) )

        else: # _____________________________________________ operator send anything else
            dp("you send me: {0}".format(value) )
            print_menu()


