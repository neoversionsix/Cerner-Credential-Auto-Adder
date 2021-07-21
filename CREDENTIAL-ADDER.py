
# This adds credentials for users based on an iput scpreadsheet
# Set Variables
users_file = 'USERS.xlsx'
creds_file = 'CREDS.xlsx'

#Import Libraries
import pyautogui
import time
import pandas as pd
import pygetwindow as gw
from ahk import AHK
ahk = AHK()
pyautogui.FAILSAFE = True

# Read Excel Files
df = pd.read_excel(users_file)
df_c = pd.read_excel(creds_file)
#Change the index
df_c.set_index('CRED', inplace=True)

# Activate HNA User Window
try:
    myWindow = gw.getWindowsWithTitle('User Maint')[0]
    myWindow.activate()
    myWindow.maximize()
except:
    print('could not maximise User Maintenance (HNA User) window')

# Switch Search Field to Username
time.sleep(0.5)
ahk.key_press('F10')
time.sleep(0.5)
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
time.sleep(0.5)
ahk.key_press('tab')
time.sleep(0.5)

# Allocate Credentials for each user
for index, row in df.iterrows():
    user = row['USERNAME']
    cred = row['CREDENTIAL']
    pyautogui.typewrite(user, interval=0.05)
    ahk.key_press('Enter')
    # Select Credential Button
    time.sleep(0.5)
    ahk.key_press('f10')
    time.sleep(0.2)
    ahk.key_press('down')
    time.sleep(0.2)
    ahk.key_press('down')
    time.sleep(0.2)
    ahk.key_press('right')
    time.sleep(0.1)
    ahk.key_press('c')
    # Click on create new credential
    time.sleep(0.5)
    ahk.key_press('tab')
    time.sleep(0.2)
    ahk.key_press('tab')
    time.sleep(0.2)
    ahk.key_press('tab')
    time.sleep(0.2)
    ahk.key_press('tab')
    time.sleep(0.2)
    ahk.key_press('down')
    time.sleep(0.2)
    ahk.key_press('tab')
    time.sleep(0.2)
    #Choose Credential based on spreadsheet
    to_type = df_c.at[cred, 'TO_TYPE']
    pyautogui.typewrite(to_type, interval=0.1)
    # Go to type of licence
    ahk.key_press('tab')
    time.sleep(0.1)
    # Choose Licence
    ahk.key_press('l')
    time.sleep(0.2)
    ahk.key_press('tab')
    time.sleep(0.05)
    ahk.key_press('tab')
    time.sleep(0.05)
    ahk.key_press('tab')
    time.sleep(0.05)
    ahk.key_press('tab')
    time.sleep(0.05)
    ahk.key_press('tab')
    time.sleep(0.05)
    ahk.key_press('tab')
    time.sleep(0.05)
    ahk.key_press('tab')
    time.sleep(0.05)
    ahk.key_press('tab')
    time.sleep(0.5)
    ahk.key_press('space')
    time.sleep(0.5)
    ahk.key_press('enter')
    time.sleep(1)
    # delete current username from searchbox
    time.sleep(0.2)
    ahk.key_press('backspace')
    ahk.key_press('backspace')
    ahk.key_press('backspace')
    ahk.key_press('backspace')
    ahk.key_press('backspace')
    ahk.key_press('backspace')
    ahk.key_press('backspace')
    ahk.key_press('backspace')
    ahk.key_press('backspace')
    ahk.key_press('backspace')