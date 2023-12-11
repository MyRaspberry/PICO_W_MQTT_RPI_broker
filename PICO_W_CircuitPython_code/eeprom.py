# get foamyguy-circuitpython-nvm-helper-7.x-mpy-1.0.2.zip !! even have i now use CP800b4
# copy  foamyguy_nvm_helper.mpy
# help from forum: Neradoc#2644

# see file settings.py and file code.py where that example is called ( but now disabled )

# ______________________________________________________________ expect file: /lib/foamyguy_nvm_helper.mpy
from foamyguy_nvm_helper import  read_data, save_data
from settings import Tuning

def get_tuning(DIAG = False) :
    if DIAG : print("NVM need /lib/foamyguy_nvm_helper.mpy ___") # ___ lib info
    try:
        tuning = read_data(verbose=False) # ____________________ get the current settings
    except Exception:
        tuning = {}

    if DIAG : print('NVM: ',tuning) # __________________________ let's see what we got ( first time,  reboot )
    return tuning

def save_tuning(tuning={},DIAG = False) : # ______________________ save back to nvm
    if DIAG : print('NVM: to save: ',tuning) # ____________________________ let's see what we got ( first time,  reboot )
    save_data(tuning, test_run=False, verbose=False )

SampleRate = 0
def testNVM() :
    global SampleRate, Tuning
    print("\n\n___ test settings.py dictionary: Tuning")
    SampleRate = Tuning.get("SampleRate",10) # _____________ get from settings.py ( imported ) 30, if not exist use default 10
    print("___ get SampleRate from settings.py from Tuning: ",SampleRate )
    Tuning = get_tuning(True) #_____________________________ overwrite Tuning from settings.py by tuning from eeprom.py and optional print it from there
    SampleRate = Tuning.get("SampleRate",10)
    print("___ get SampleRate from Tuning from NVM: ",SampleRate )

    SampleRate = 36 #_______________________________________ TEST: now we change that value
    print("___ local overwrite SampleRate: ",SampleRate )
    Tuning["SampleRate"] = SampleRate # ____________________ save to dictionary
    print("___ saved to Tuning: ",Tuning )
    save_tuning(Tuning,True) # _____________________________ save to NVM

    print("\n___ end useNVM\n")
