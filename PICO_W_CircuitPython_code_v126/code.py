# KLL
# file: code.py
# board: PICO W RP2040
# for revision see 'settings.toml'

# JOB1 Analog read 3 channel + CPU Temp
# JOB2 DHT22 sensor
# JOB3 INA219 sensor
# JOB4 ADS1115 sensor
# JOB5 MQTT send
# JOB6 User-Spare

# JOB and MENU structure

# web server ( see 'settings.toml' file )
# data page

# move OSCI out to extra project 2022-12-11, but include again as pms1w
# ( use: [ctrl][c] import pms1w for stop that [ctrl][c] [ctrl][d] not always work)


# ______________________________________________________ expect a file jobs.py
from jobs import dp

import gc # micropython garbage collection # use gc.mem_free() # use gc.collect()
def check_mem() :
    dp(f"___ check mem : {gc.mem_free()} ")
    gc.collect()
    dp(f"___ after clear : {gc.mem_free()} ")

# ______________________________________________________ expect a file web_wifi.py
from web_wifi import setup_webserver, run_webserver
setup_webserver()

# ______________________________________________________ expect a file settings.py
from settings import Tuning

useNVM = False #True
# ______________________________________________________ expect a file eeprom.py
# disable NVM for CP900 until new version...
#if useNVM : from eeprom import get_tuning, save_tuning, testNVM
#if useNVM : testNVM()

import time # _________________________________________ we use time.monotonic aka seconds in float, to control the loop and NO time.sleep() any more..
print(f"\nFREE MEM report from CODE.PY after imports\n+ import time {gc.mem_free()}")

# ______________________________________________________ expect a file jobs.py
from jobs import console, print_menu, get_JOB0en, get_JOB1en, get_JOB2en, get_JOB3en, get_JOB4en, get_JOB5en, get_JOB6en, get_DIAG
from jobs import get_update0, get_update1, get_update2, get_update3, get_update4, get_update5, get_update6


# ______________________________________________________ expect a file jobs.py
from jobs import JOB0
JOB0en = False # _______________________________________ from JOB0 but written by menu.console, get later
from jobs import JOB1
JOB1en = False # _______________________________________ from JOB1 but written by menu.console, get later
from jobs import JOB2
JOB2en = False # _______________________________________ from JOB2 but written by menu.console, get later
from jobs import JOB3
JOB3en = False # _______________________________________ from JOB3 but written by menu.console, get later
from jobs import JOB4
JOB4en = False # _______________________________________ from JOB4 but written by menu.console, get later
from jobs import JOB5
JOB5en = False # _______________________________________ from JOB5 but written by menu.console, get later
from jobs import JOB6
JOB6en = False # _______________________________________ from JOB6 but written by menu.console, get later

# ______________________________________________________ JOB1 user program timer
greeting = "___ JOB TIMER & MENU ___"
loop1 = 0
loopt1 = 10 # _________________________________________ we can read time every loop OR every loopt loop only, makes the 1M faster (26s to 31s)/ but timer more inaccurate
update1 = get_update1() # ______________________________ every .. sec do
clock1 = 0  # __________________________________________ count main sec interval

# ______________________________________________________ JOB2 user program timer
loop2 = 200
loopt2 = 100 # ________________________________________ we can read time every loop OR every loopt loop only, makes the 1M faster (26s to 31s)/ but timer more inaccurate
update2 = get_update2() # ______________________________ every .. sec do
clock2 = 0  # __________________________________________ count main sec interval

# ______________________________________________________ JOB3 user program timer
loop3 = 300
loopt3 = 500 # _________________________________________ we can read time every loop OR every loopt loop only, makes the 1M faster (26s to 31s)/ but timer more inaccurate
update3 = get_update3() # ______________________________ every .. sec do
clock3 = 0  # __________________________________________ count main sec interval

# ______________________________________________________ JOB4 user program timer
loop4 = 400
loopt4 = 1000 # ________________________________________ we can read time every loop OR every loopt loop only, makes the 1M faster (26s to 31s)/ but timer more inaccurate
update4 = get_update4() # ______________________________ every .. sec do
clock4 = 0  # __________________________________________ count main sec interval

# ______________________________________________________ JOB5 user program timer
loop5 = 500
loopt5 = 100 # ________________________________________ we can read time every loop OR every loopt loop only, makes the 1M faster (26s to 31s)/ but timer more inaccurate
update5 = get_update5() # ______________________________ every .. sec do
clock5 = 0  # __________________________________________ count main sec interval

# ______________________________________________________ JOB6 user program timer
loop6 = 600
loopt6 = 1000 # ________________________________________ we can read time every loop OR every loopt loop only, makes the 1M faster (26s to 31s)/ but timer more inaccurate
update6 = get_update6() # ______________________________ every .. sec do
clock6 = 0  # __________________________________________ count main sec interval

# ______________________________________________________ JOB0 program counter, every n loops do
loop0 = 0
loopt0 =300 # __________________________________________ do JOBSYS every .. loops
update0 = 0.5 # ________________________________________ do JOB0 every second

def JOBSYS() : # _________________________________________ in here call webserver updates...
    global JOB0en, JOB1en,JOB2en,JOB3en,JOB4en,JOB5en,JOB6en,DIAG # so we can get it after modified by menu operation
    global update0, update1, update2, update3, update4, update5, update6
    if False : # _______________________________________ for first test only used
        dp("#", end="")
    console() # ________________________________________ file: menu.py, manual input in REPL checked / must finish with [ENTER] or it blocks
    JOB0en=get_JOB0en()
    update0 = get_update0()
    JOB1en=get_JOB1en() # readback if operated
    update1 = get_update1()
    JOB2en=get_JOB2en()
    update2 = get_update2()
    JOB3en=get_JOB3en()
    update3 = get_update3()
    JOB4en=get_JOB4en()
    update4 = get_update4()
    JOB5en=get_JOB5en()
    update5 = get_update5()
    JOB6en=get_JOB6en()
    update6 = get_update6()
    DIAG=get_DIAG()



# ______________________________________________________ setup NO BLOCKING main loop structure
# time.monotonic is seconds as float

start_s0 = time.monotonic()
start_s1 = time.monotonic()
start_s2 = time.monotonic()
start_s3 = time.monotonic()
start_s4 = time.monotonic()
start_s5 = time.monotonic()
start_s6 = time.monotonic()

Mloop_s = time.monotonic()
last_Mloop_s = time.monotonic()
loopM = 0
Mlooprep = True
secdotprint = True

dp(greeting)
check_mem()
print_menu()
while True: # ___________________________________________ MAIN
    try:
        loop0 += 1
        if loop0 >= loopt0 : # __________________________ call JOBSYS
            loop0 = 0
            JOBSYS() # __________________________________ there can call webserver / mqtt updates / jobs-menu operation
            now_s0 = time.monotonic()   # _______________ JOB0 is a timed job
            if now_s0 >= (start_s0 + update0 ):  # ______ 1/2 sec
                start_s0 = now_s0
                if JOB0en: JOB0() # ________________________________ DIO job

        loop1 += 1
        if loop1 > loopt1 :
            loop1 = 0
            now_s1 = time.monotonic()   # _______________ JOB1 is a timed job, but use a counter to NOT read millis every loop as that's slow
            if now_s1 >= (start_s1 + 1.0):  # ___________ 1 sec
                start_s1 = now_s1
                if secdotprint :
                    dp(".", "") # means print(".",end="") aka NO LINEFEED
                run_webserver() # __________________________________ update if someone called our page moved from JOB SYS to 1sec here
                #check_mem()
                clock1 += 1
                if clock1 >= update1:
                    clock1 = 0
                    if JOB1en : JOB1() # _______________ call the user program after timed seconds

        loop2 += 1
        if loop2 > loopt2 :
            loop2 = 0
            now_s2 = time.monotonic()   # ______________ JOB2 is a timed job, but use a counter to NOT read millis every loop as thats slow
            if now_s2 >= (start_s2 + 1.0):  # __________ 1 sec
                start_s2 = now_s2
                clock2 += 1
                if clock2 >= update2:
                    clock2 = 0
                    if JOB2en : JOB2() # _______________ call the user program after timed seconds

        loop3 += 1
        if loop3 > loopt3 :
            loop3 = 0
            now_s3 = time.monotonic()   # ______________ JOB3 is a timed job, but use a counter to NOT read millis every loop as thats slow
            if now_s3 >= (start_s3 + 1.0):  # __________ 1 sec
                start_s3 = now_s3
                clock3 += 1
                if clock3 >= update3:
                    clock3 = 0
                    if JOB3en : JOB3() # _______________ call the user program after timed seconds

        loop4 += 1
        if loop4 > loopt4 :
            loop4 = 0
            now_s4 = time.monotonic()   # ______________ JOB4 is a timed job, but use a counter to NOT read millis every loop as thats slow
            if now_s4 >= (start_s4 + 1.0):  # __________ 1 sec
                start_s4 = now_s4
                clock4 += 1
                if clock4 >= update4:
                    clock4 = 0
                    if JOB4en : JOB4() # _______________ call the user program after timed seconds

        loop5 += 1
        if loop5 > loopt5 :
            loop5 = 0
            now_s5 = time.monotonic()   # ______________ JOB5 is a timed job, but use a counter to NOT read millis every loop as thats slow
            if now_s5 >= (start_s5 + 1.0):  # __________ 1 sec
                start_s5 = now_s5
                clock5 += 1
                update5 = get_update5() # from menu !!
                #dp(" code: loop 5 update5: {:d}".format (update5) )
                if clock5 >= update5:
                    clock5 = 0
                    if JOB5en : JOB5() # _______________ call the user program after timed seconds

        loop6 += 1
        if loop6 > loopt6 :
            loop6 = 0
            now_s6 = time.monotonic()   # ______________ JOB6 is a timed job, but use a counter to NOT read millis every loop as thats slow
            if now_s6 >= (start_s6 + 1.0):  # __________ 1 sec
                start_s6 = now_s6
                clock6 += 1
                if clock6 >= update6:
                    clock6 = 0
                    if JOB6en : JOB6() # _______________ call the user program after timed seconds

        loopM += 1
        if loopM >= 1000000: # _________________________ 1 million loop timer / reporter
            loopM = 0
            Mloop_s = time.monotonic()
            #if Mlooprep: dp("\n___ 1Mloop: {:>5.2f} sec, available heap RAM {:} ".format( (Mloop_s - last_Mloop_s), gc.mem_free() ) )
            if Mlooprep: dp("\n___ 1Mloop: {:>5.2f} sec ".format( (Mloop_s - last_Mloop_s) ) )
            last_Mloop_s = Mloop_s  # __________________ remember
            check_mem()

    except OSError:
        continue

dp("___ end") # ________________________________________ never gonna happen
