# Import your libraries
import tkinter as tk
from tkinter import messagebox
import threading
import sys
import pyautogui
import pygetwindow as gw
from ahk import AHK
import tkinter.font as tkFont
import pyperclip

#GLOBAL VARIABLES
# Global flag to control script execution
script_running = False
stop_event = threading.Event()
#Delays
username_text = "credentialbox"
SHORT_DELAY = 0.2
LONG_DELAY = 1
# Create an AHK object
ahk = AHK()

#GLOBAL FUNCTIONS
class ScriptTerminated(Exception):
    pass

def ensure_running():
    if not script_running or stop_event.is_set():
        raise ScriptTerminated

def sleep_with_cancel(delay):
    ensure_running()
    if stop_event.wait(max(0, delay)):
        raise ScriptTerminated

def press_key(key):
    ensure_running()
    ahk.key_press(key)

# Function to press a key with a short delay
def press_key_with_delay(key, delay=SHORT_DELAY):
    press_key(key)
    sleep_with_cancel(delay)
# Function to press the Tab key a specified number of times
def press_tab(num_times):
    for _ in range(num_times):
        press_key_with_delay('tab')

# Paste text with a short settle delay for clipboard + UI processing
def paste_text(text, select_all=False, pre_delay=0.08, post_delay=0.35):
    ensure_running()
    pyperclip.copy(text)
    sleep_with_cancel(pre_delay)
    if select_all:
        pyautogui.hotkey('ctrl', 'a', interval=0.05)
        sleep_with_cancel(0.05)
    ensure_running()
    pyautogui.hotkey('ctrl', 'v', interval=0.05)
    sleep_with_cancel(post_delay)
# Function to terminate the script
def terminate_script():
    global script_running
    script_running = False  # Set the flag to False to stop the script
    stop_event.set()

def run_with_termination_handling(func):
    def wrapper(*args, **kwargs):
        global script_running
        script_running = True
        stop_event.clear()
        pyautogui.FAILSAFE = True
        try:
            return func(*args, **kwargs)
        except ScriptTerminated:
            print("Script terminated by user.")
        finally:
            script_running = False
    return wrapper

# Redirect stdout to the Text widget
class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)

    def flush(self):
        pass

# Function that contains your script
@run_with_termination_handling
def start_script(start_day, start_month, start_year, credentials_to_add):
    # ... (Your script goes here, using the passed values of start_day, etc.)
    # This adds credentials to the pool for the credential box
    # Activate HNA User Window
    #region
    for _ in range(3):  # Try 3 times
        try:
            myWindow = gw.getWindowsWithTitle('User Maint')[0]
            myWindow.activate()
            break  # If activation is successful, break the loop
        except Exception:
            print('Attempt to activate User Maintenance window failed. Retrying...')
            sleep_with_cancel(0.5)  # Wait for a half second before retrying
    else:
        print('Could not activate User Maintenance window after 3 attempts. Terminating application...')
        root.destroy()  # Close the application
        return  # Exit the function
    #endregion
    # Switch Search Field to Username
    sleep_with_cancel(SHORT_DELAY)
    press_key('F10')
    sleep_with_cancel(SHORT_DELAY)
    press_key('down')
    sleep_with_cancel(SHORT_DELAY)
    press_key('down')
    sleep_with_cancel(SHORT_DELAY)
    press_key('down')
    sleep_with_cancel(SHORT_DELAY)
    press_key('down')
    sleep_with_cancel(SHORT_DELAY)
    press_key('right')
    sleep_with_cancel(SHORT_DELAY)
    press_key('down')
    sleep_with_cancel(SHORT_DELAY)
    press_key('enter')
    sleep_with_cancel(SHORT_DELAY)
    # Open Credential Box   
    sleep_with_cancel(SHORT_DELAY)
    press_key('Space')
    press_key('Backspace')
    print("Script is running")
    paste_text(username_text)
    #pyautogui.typewrite("credentialbox", interval = SHORT_DELAY)
    press_key('Enter')
    print("Credential Box Opened")
    # Select Credential Button
    sleep_with_cancel(LONG_DELAY)
    press_key_with_delay('f10')
    press_key_with_delay('down')
    press_key_with_delay('down')
    press_key_with_delay('right')
    press_key_with_delay('c')
    sleep_with_cancel(LONG_DELAY)
    count = int(0)
    while count < credentials_to_add and script_running:  
        # Click on create new credential
        print("Creds Created: ", count)
        if count == 0:
            sleep_with_cancel(SHORT_DELAY)
            press_tab(4)
            sleep_with_cancel(SHORT_DELAY)
            press_key('down')
            sleep_with_cancel(SHORT_DELAY)
            press_key('tab')
            sleep_with_cancel(SHORT_DELAY)
        else:
            sleep_with_cancel(SHORT_DELAY)
            press_tab(2)
            sleep_with_cancel(SHORT_DELAY)
            press_key('down')
            sleep_with_cancel(SHORT_DELAY)
            press_key('tab')
            sleep_with_cancel(SHORT_DELAY)
        #Choose Credential
        to_type = 'a'
        ensure_running()
        pyautogui.typewrite(to_type, interval=0.1)
        sleep_with_cancel(SHORT_DELAY)
        # Go to type of licence
        press_key('tab')
        sleep_with_cancel(0.4)
        # Choose Licence
        press_key('l')
        sleep_with_cancel(SHORT_DELAY)
        press_tab(4)
        sleep_with_cancel(SHORT_DELAY)
        # Enter date
        day = "{0:0=2d}".format(start_day) # convert two digit
        month = "{0:0=2d}".format(start_month) # convert two digit
        year = str(start_year) # year to string
        date_text = day + month + year
        paste_text(date_text, post_delay=0.5)
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
        sleep_with_cancel(SHORT_DELAY)
        press_tab(7)
        sleep_with_cancel(SHORT_DELAY)
        press_key('enter')
        sleep_with_cancel(2)
        # delete credential
        press_tab(2)
        sleep_with_cancel(SHORT_DELAY)
        press_key('space')
        sleep_with_cancel(SHORT_DELAY)
        press_tab(2)
        sleep_with_cancel(SHORT_DELAY)
        press_key('enter')
        # Apply deletion
        sleep_with_cancel(SHORT_DELAY)
        press_tab(2)
        sleep_with_cancel(SHORT_DELAY)
        press_key('enter')
        sleep_with_cancel(1)
        count +=1

# Function to run the script in a separate thread
def run_script():
    if script_running:
        messagebox.showwarning("Script Running", "The script is already running.")
        return
    try:
        # Retrieve values from the GUI
        start_day = int(day_entry.get())
        start_month = int(month_entry.get())
        start_year = int(year_entry.get())
        credentials_to_add = int(users_entry.get())

        # Start the script in a new thread
        script_thread = threading.Thread(target=start_script, args=(start_day, start_month, start_year, credentials_to_add))
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

tk.Label(root, text="Credentials to Add:").grid(row=3, column=0)
users_entry = tk.Entry(root)
users_entry.grid(row=3, column=1)

# Create and layout buttons
start_button = tk.Button(root, text="Start", command=run_script)
start_button.grid(row=4, column=0, columnspan=2)
# Create a custom font
custom_font = tkFont.Font(family="Helvetica", size=16, weight="bold")

terminate_button = tk.Button(root, text="CLICK TO TERMINATE SCRIPT", command=terminate_script,
                             font=custom_font, bg="red", fg="white",
                             height=20, width=50, padx=10, pady=10)
terminate_button.grid(row=5, column=0, columnspan=2)

# Create a Text widget for the console at the bottom of the GUI
console = tk.Text(root)
console.grid(row=7, column=0, columnspan=2)

# Redirect stdout and stderr
sys.stdout = TextRedirector(console)
sys.stderr = TextRedirector(console)

# Start the GUI event loop
root.mainloop()
