"""
GUIADDER_noAHK.py

This script uses pure PyAutoGUI for keyboard and mouse automation instead of AutoHotkey.
It also uses pygetwindow to activate a specific window by title ("User Maint").
Finally, it provides a Tkinter GUI for user input and to start/stop the automation.
"""

import tkinter as tk
from tkinter import messagebox
import threading
import sys
import pyautogui
import time
import pygetwindow as gw
import tkinter.font as tkFont

# --------------- GLOBAL VARIABLES ---------------
script_running = False      # Global flag to control script execution
SHORT_DELAY = 0.2
LONG_DELAY = 1

# --------------- GLOBAL FUNCTIONS ---------------

def press_key_with_delay(key, delay=SHORT_DELAY):
    """
    Presses a key using PyAutoGUI and then waits for 'delay' seconds.
    Example keys: 'enter', 'tab', 'f10', 'space', 'backspace', etc.
    """
    pyautogui.press(key)
    time.sleep(delay)

def press_tab(num_times):
    """
    Press the Tab key 'num_times' times, each with a short delay.
    """
    for _ in range(num_times):
        press_key_with_delay('tab')

def terminate_script():
    """
    Sets the global 'script_running' flag to False, which stops the automation loop.
    """
    global script_running
    script_running = False

class TextRedirector(object):
    """
    Redirects 'print' output to the Tkinter Text widget for display.
    """
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)

    def flush(self):
        pass

def start_script(start_day, start_month, start_year, credentials_to_add):
    """
    The main automation script.
    - Activates the "User Maint" window using pygetwindow.
    - Uses PyAutoGUI to type, press keys (F10, Tab, etc.), and move through the workflow.
    - Adds credentials in a loop until the specified count is reached or user terminates.
    """
    global script_running
    script_running = True  # Flag on
    pyautogui.FAILSAFE = True  # Raise an exception if the mouse is moved to a screen corner

    # Try up to 3 times to activate the window with title "User Maint"
    for _ in range(3):
        try:
            my_window = gw.getWindowsWithTitle('User Maint')[0]
            my_window.activate()
            break
        except:
            print('Attempt to activate User Maintenance window failed. Retrying...')
            time.sleep(0.5)
    else:
        print('Could not activate User Maintenance window after 3 attempts. Terminating application...')
        root.destroy()
        return

    # Switch Search Field to Username (emulates the original AHK sequence)
    time.sleep(SHORT_DELAY)
    press_key_with_delay('f10')
    press_key_with_delay('down')
    press_key_with_delay('down')
    press_key_with_delay('down')
    press_key_with_delay('down')
    press_key_with_delay('right')
    press_key_with_delay('down')
    press_key_with_delay('enter')
    time.sleep(SHORT_DELAY)
    press_key_with_delay('tab')

    # Open Credential Box  
    time.sleep(SHORT_DELAY)
    pyautogui.press('space')
    pyautogui.press('backspace')

    if script_running:
        print("Script is running")
        pyautogui.typewrite("credentialbox", interval=0.1)
        press_key_with_delay('enter')
        print("Credential Box Opened")

        # Select Credential Button
        time.sleep(LONG_DELAY)
        press_key_with_delay('f10')
        press_key_with_delay('down')
        press_key_with_delay('down')
        press_key_with_delay('right')
        press_key_with_delay('c')
        time.sleep(LONG_DELAY)
        count = 0
    else:
        print("Script terminated by user.")
        return

    # Main loop to add credentials
    while count < credentials_to_add and script_running:
        print("Creds Created:", count)
        if count == 0:
            time.sleep(SHORT_DELAY)
            press_tab(4)
            time.sleep(SHORT_DELAY)
            pyautogui.press('down')
            time.sleep(SHORT_DELAY)
            pyautogui.press('tab')
            time.sleep(SHORT_DELAY)
        else:
            time.sleep(SHORT_DELAY)
            press_tab(2)
            time.sleep(SHORT_DELAY)
            pyautogui.press('down')
            time.sleep(SHORT_DELAY)
            pyautogui.press('tab')
            time.sleep(SHORT_DELAY)

        if not script_running:
            print("Script terminated by user.")
            break

        # Choose Credential
        to_type = 'a'
        pyautogui.typewrite(to_type, interval=0.1)
        time.sleep(SHORT_DELAY)

        # Go to type of license
        pyautogui.press('tab')
        time.sleep(0.4)
        # Choose license
        pyautogui.press('l')
        time.sleep(SHORT_DELAY)
        press_tab(4)
        time.sleep(SHORT_DELAY)

        # Enter date
        day_str = "{0:0=2d}".format(start_day)
        month_str = "{0:0=2d}".format(start_month)
        year_str = str(start_year)

        pyautogui.typewrite(day_str, interval=0.1)
        pyautogui.typewrite(month_str, interval=0.1)
        pyautogui.typewrite(year_str, interval=0.1)

        # Increment date logic
        start_day += 1
        if start_day > 25:
            start_day = 1
            start_month += 1
        if start_month > 12:
            start_day = 1
            start_month = 1
            start_year += 1

        # Hit Apply
        time.sleep(SHORT_DELAY)
        press_tab(7)
        time.sleep(SHORT_DELAY)
        pyautogui.press('enter')
        time.sleep(2)

        # Delete credential
        press_tab(2)
        time.sleep(SHORT_DELAY)
        pyautogui.press('space')
        time.sleep(SHORT_DELAY)
        press_tab(2)
        time.sleep(SHORT_DELAY)
        pyautogui.press('enter')

        # Apply deletion
        time.sleep(SHORT_DELAY)
        press_tab(2)
        time.sleep(SHORT_DELAY)
        pyautogui.press('enter')
        time.sleep(1)

        count += 1

    print("Script finished or terminated by user.")

def run_script():
    """
    Reads user input from the Tkinter Entry fields, then starts 'start_script' in a new thread.
    """
    try:
        start_day = int(day_entry.get())
        start_month = int(month_entry.get())
        start_year = int(year_entry.get())
        credentials_to_add = int(users_entry.get())

        script_thread = threading.Thread(
            target=start_script,
            args=(start_day, start_month, start_year, credentials_to_add)
        )
        script_thread.start()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# ---------------- TKINTER GUI SETUP ----------------
root = tk.Tk()
root.title("Credential Script")

# Create and layout input fields
tk.Label(root, text="Start Day:").grid(row=0, column=0, sticky="e")
day_entry = tk.Entry(root)
day_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Start Month:").grid(row=1, column=0, sticky="e")
month_entry = tk.Entry(root)
month_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Start Year:").grid(row=2, column=0, sticky="e")
year_entry = tk.Entry(root)
year_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Credentials to Add:").grid(row=3, column=0, sticky="e")
users_entry = tk.Entry(root)
users_entry.grid(row=3, column=1, padx=5, pady=5)

# Create and layout buttons
start_button = tk.Button(root, text="Start", command=run_script)
start_button.grid(row=4, column=0, columnspan=2, pady=5)

# Larger "Terminate" button
custom_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
terminate_button = tk.Button(
    root, text="CLICK TO TERMINATE SCRIPT",
    command=terminate_script,
    font=custom_font, bg="red", fg="white",
    height=2, width=30
)
terminate_button.grid(row=5, column=0, columnspan=2, pady=10)

# Console output box
console = tk.Text(root, height=10, width=50)
console.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Redirect stdout and stderr to the console text widget
sys.stdout = TextRedirector(console)
sys.stderr = TextRedirector(console)

# Start the GUI loop
root.mainloop()