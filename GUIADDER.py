import tkinter as tk
from tkinter import messagebox
import threading

# Import your libraries
import pyautogui
import time
import keyboard
import pygetwindow as gw
from ahk import AHK

# Global flag to control script execution
script_running = False

def terminate_script():
    global script_running
    script_running = False  # Set the flag to False to stop the script

# Function that contains your script
def start_script(start_day, start_month, start_year, users_to_add):
    # ... (Your script goes here, using the passed values of start_day, etc.)
    # This adds credentials to the pool for the credential box
    # Set Initial Variables
    global script_running
    script_running = True  # Set the flag to True when the script starts
    ahk = AHK()
    pyautogui.FAILSAFE = True

    # Activate HNA User Window
    ahk.click(80,1060)
    time.sleep(1)
    # Switch Search Field to Username
    ahk.key_press('F10')
    time.sleep(0.3)
    ahk.key_press('down')
    time.sleep(0.3)
    ahk.key_press('down')
    time.sleep(0.3)
    ahk.key_press('down')
    time.sleep(0.3)
    ahk.key_press('down')
    time.sleep(0.3)
    ahk.key_press('right')
    time.sleep(0.3)
    ahk.key_press('down')
    time.sleep(0.3)
    ahk.key_press('enter')
    time.sleep(0.3)
    ahk.key_press('tab')
    time.sleep(0.3)
    # Open Credential Box
    user = 'credentialbox'
    if script_running == True:
        pyautogui.typewrite(user, interval=0.1)
        ahk.key_press('Enter')
        # Select Credential Button
        time.sleep(1)
        ahk.key_press('f10')
        time.sleep(0.3)
        ahk.key_press('down')
        time.sleep(0.3)
        ahk.key_press('down')
        time.sleep(0.3)
        ahk.key_press('right')
        time.sleep(0.3)
        ahk.key_press('c')
        time.sleep(1)
        count = int(0)
    else:
        print("Script terminated by user.")        
    while count < users_to_add and script_running:  
        # Click on create new credential
        if count == 0:
            time.sleep(0.3)
            ahk.key_press('tab')
            time.sleep(0.3)
            ahk.key_press('tab')
            time.sleep(0.3)
            ahk.key_press('tab')
            time.sleep(0.3)
            ahk.key_press('tab')
            time.sleep(0.3)
            ahk.key_press('down')
            time.sleep(0.3)
            ahk.key_press('tab')
            time.sleep(0.3)
        else:
            time.sleep(0.3)
            ahk.key_press('tab')
            time.sleep(0.3)
            ahk.key_press('tab')
            time.sleep(0.3)
            ahk.key_press('down')
            time.sleep(0.3)
            ahk.key_press('tab')
            time.sleep(0.3)
        if not script_running:
            print("Script terminated by user.")
            break
        #Choose Credential
        to_type = 'a'
        pyautogui.typewrite(to_type, interval=0.1)
        time.sleep(0.3)
        # Go to type of licence
        ahk.key_press('tab')
        time.sleep(0.4)
        # Choose Licence
        ahk.key_press('l')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
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
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('enter')
        time.sleep(2)
        # delete credential
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('space')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('enter')
        # Apply deletion
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('tab')
        time.sleep(0.3)
        ahk.key_press('enter')
        time.sleep(1)
        count +=1
        if not script_running:
            print("Script terminated by user.")
            break

# Function to run the script in a separate thread
def run_script():
    try:
        # Retrieve values from the GUI
        start_day = int(day_entry.get())
        start_month = int(month_entry.get())
        start_year = int(year_entry.get())
        users_to_add = int(users_entry.get())

        # Start the script in a new thread
        script_thread = threading.Thread(target=start_script, args=(start_day, start_month, start_year, users_to_add))
        script_thread.start()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers")

# Create the main window
root = tk.Tk()
root.title("Credential Script")

# Create and layout input fields
tk.Label(root, text="Start Day:").grid(row=0, column=0)
day_entry = tk.Entry(root)
day_entry.grid(row=0, column=1)

tk.Label(root, text="Start Month:").grid(row=1, column=0)
month_entry = tk.Entry(root)
month_entry.grid(row=1, column=1)

tk.Label(root, text="Start Year:").grid(row=2, column=0)                

year_entry = tk.Entry(root)
year_entry.grid(row=2, column=1)

tk.Label(root, text="Users to Add:").grid(row=3, column=0)
users_entry = tk.Entry(root)
users_entry.grid(row=3, column=1)

# Create and layout buttons
start_button = tk.Button(root, text="Start", command=run_script)
start_button.grid(row=4, column=0, columnspan=2)

terminate_button = tk.Button(root, text="Terminate", command=terminate_script)
terminate_button.grid(row=5, column=0, columnspan=2)

# Start the GUI event loop
root.mainloop()
