# This adds credentials to the pool for the credential box
# Asks user for year and users to add

start_day = 1
start_month = 1
#start_year = 1904
#users_to_add = 100

users_to_add = int(input('how many users do you want to add?'))
print('Be aware a user can not have a duplicate credential with the same start date')
start_year = int(input('what year shall the creds start at (choose a year before 2018)?'))

# IMPORT LIBRARIES
import pyautogui
import time
import pygetwindow as gw
from ahk import AHK
ahk = AHK()
pyautogui.FAILSAFE = True
# Activate HNA User Window
try:
    myWindow = gw.getWindowsWithTitle('User Maint')[0]
    myWindow.activate()
    myWindow.maximize()
except:
    print('could not maximise User Maintenance window')
time.sleep(1)
# Switch Search Field to Username
ahk.key_press('F10')
time.sleep(0.1)
ahk.key_press('down')
time.sleep(0.1)
ahk.key_press('down')
time.sleep(0.1)
ahk.key_press('down')
time.sleep(0.1)
ahk.key_press('down')
time.sleep(0.1)
ahk.key_press('right')
time.sleep(0.1)
ahk.key_press('down')
time.sleep(0.1)
ahk.key_press('enter')
time.sleep(0.1)
ahk.key_press('tab')
time.sleep(0.1)
# Open Credential Box
user = 'credentialbox'
pyautogui.typewrite(user, interval=0.1)
ahk.key_press('Enter')
# Select Credential Button
time.sleep(1)
ahk.key_press('f10')
time.sleep(0.1)
ahk.key_press('down')
time.sleep(0.1)
ahk.key_press('down')
time.sleep(0.1)
ahk.key_press('right')
time.sleep(0.1)
ahk.key_press('c')
time.sleep(1)
count = int(0)
while count < users_to_add:  
    # Click on create new credential
    if count == 0:
        time.sleep(0.1)
        ahk.key_press('tab')
        time.sleep(0.1)
        ahk.key_press('tab')
        time.sleep(0.1)
        ahk.key_press('tab')
        time.sleep(0.1)
        ahk.key_press('tab')
        time.sleep(0.1)
        ahk.key_press('down')
        time.sleep(0.1)
        ahk.key_press('tab')
        time.sleep(0.1)
    else:
        time.sleep(0.1)
        ahk.key_press('tab')
        time.sleep(0.1)
        ahk.key_press('tab')
        time.sleep(0.1)
        ahk.key_press('down')
        time.sleep(0.1)
        ahk.key_press('tab')
        time.sleep(0.1)     
    #Choose Credential
    to_type = 'a'
    pyautogui.typewrite(to_type, interval=0.1)
    time.sleep(0.1)
    # Go to type of licence
    ahk.key_press('tab')
    time.sleep(0.4)
    # Choose Licence
    ahk.key_press('l')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    # Enter date
    day = "{0:0=2d}".format(start_day) # convert two digit
    month = "{0:0=2d}".format(start_month) # convert two digit
    year = str(start_year) # year to string
    pyautogui.typewrite(day, interval=0.1)
    pyautogui.typewrite(month, interval=0.1)
    pyautogui.typewrite(year, interval=0.1)
    # Get date for next round
    start_day +=1
    if start_day > 25:
        start_day = int(1)
        start_month += 1
    if start_month > 12:
        start_day = 1
        start_month = 1
        start_year +=1
    # Hit Apply
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('enter')
    time.sleep(2)
    # delete credential
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('space')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('enter')
    # Apply deletion
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('tab')
    time.sleep(0.1)
    ahk.key_press('enter')
    time.sleep(1)
    count +=1