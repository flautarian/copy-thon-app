"""Py replay actions

This script provides a graphical user interface (GUI) for recording and replaying user actions 
in a Python application. It allows users to record their actions, replay them, and manage the recorded files.

The script utilizes Tkinter for the GUI, PIL for image handling, and other modules for various functionalities related by the mouse and keyboard control.

Author: Facundo Giacconi AKA "GiacconiDev"

"""

# Import necessary modules
from tkinter import *
import os
from tkinter.messagebox import askyesno
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
import logging
from floating_message import FloatingMessage

import options
from record import start_record_events_thread
from replay import start_replay_events_thread
from utils import FONT_NAME, GREEN, SCRIPT_DIR, YELLOW

# Initialize TK
window = Tk()

# Constants
ARROW_IMG = Image.open(f"{SCRIPT_DIR}/img/arrow-one.png").resize((40,40), Image.LANCZOS)
ARROW_TK = ImageTk.PhotoImage(ARROW_IMG)

RECORD_IMG = Image.open(f"{SCRIPT_DIR}/img/record.png").resize((40,40), Image.LANCZOS)
RECORD_TK = ImageTk.PhotoImage(RECORD_IMG)

PLAY_IMG = Image.open(f"{SCRIPT_DIR}/img/play.png").resize((40,40), Image.LANCZOS)
PLAY_TK = ImageTk.PhotoImage(PLAY_IMG)

DELETE_IMG = Image.open(f"{SCRIPT_DIR}/img/delete.png").resize((40,40), Image.LANCZOS)
DELETE_TK = ImageTk.PhotoImage(DELETE_IMG)

GEAR_IMG = Image.open(f"{SCRIPT_DIR}/img/gear.png").resize((40,40), Image.LANCZOS)
GEAR_TK = ImageTk.PhotoImage(GEAR_IMG)

LOOP_ARROW_IMG = Image.open(f"{SCRIPT_DIR}/img/arrow-repeat.png").resize((40,40), Image.LANCZOS)
LOOP_ARROW_TK = ImageTk.PhotoImage(LOOP_ARROW_IMG)

reps = 0
timer = None

# Action Listener to Register Movements
logging.basicConfig(level=logging.DEBUG)

looping_check = False


def open_options():
    """Open Options
    
    Opens the options window for configuring settings.
    """
    options.open_options(window)
    
def delete_current_file():
    """Delete Current File
    
    Deletes the currently selected file from the data folder.
    """
    answer = askyesno(options.get_i18n_literal('delete'), options.get_i18n_literal('confirm'))
    current_file = file_selector.get()
    if answer == True and current_file is not None and current_file != "":
        os.remove(f"{SCRIPT_DIR}/data/{current_file}")
        refresh_file_selector()
        logging.info(f"deleted file:{current_file}")

def update_data_folder():
    """Update Data Folder
    
    Updates the list of files in the data folder.
    """
    folder_files = os.listdir(f"{SCRIPT_DIR}/data")
    logging.info(f"updating data folder elements to {folder_files}")
    return folder_files


def toggle_looping_mode():
    """Toggle Looping Mode
    
    Toggles looping mode for replaying actions.
    """
    global looping_check
    
    looping_check = not looping_check
    if looping_check is False:
        result = ARROW_TK
    else:
        result = LOOP_ARROW_TK
    
    logging.info(f"toggling repeat mode to {looping_check}")
    
    record_loop_btn.config(image=result)
            
            
def refresh_file_selector():
    """Refresh File Selector
    
    Refreshes the file selector Combobox with updated data from the data folder.
    """
    global file_selector, delete_btn, play_btn, record_loop_btn
    
    file_selector['values'] = update_data_folder()
    if len(file_selector['values']) > 0:
        file_selector.current(0)
        delete_btn.config(state="active")
        play_btn.config(state="active")
        record_loop_btn.config(state="active")
    else:
        file_selector.set('')
        delete_btn.config(state="disabled")
        play_btn.config(state="disabled")
        record_loop_btn.config(state="disabled")

# UI Setup

if __name__ == "__main__":
    window.title("Py replay actions")
    window.config(padx=10, pady=5, bg=YELLOW)
    
    # elements declaration
    record_btn = Button(image=RECORD_TK, command=lambda: start_record_events_thread([play_btn, record_btn, record_loop_btn, delete_btn, options_btn], window, refresh_file_selector))
    record_btn.grid(column=0, row=1)

    record_loop_btn = Button(image=ARROW_TK, bg=YELLOW, fg=GREEN, justify="center", command=toggle_looping_mode)
    record_loop_btn.grid(column=1, row=1)

    # Generating Combobox with loaded files
    file_selector_var = StringVar()
    file_selector = Combobox(state = 'readonly', textvariable=file_selector_var)
    file_selector.grid(column=2, row=1, sticky="ew")

    play_btn = Button(image=PLAY_TK, command= lambda: start_replay_events_thread([play_btn, record_btn, record_loop_btn, delete_btn, options_btn], file_selector.get(), window, looping_check), justify="left")
    play_btn.grid(column=3, row=1)

    delete_btn = Button(image=DELETE_TK, command= delete_current_file, justify="center")
    delete_btn.grid(column=4, row=1)

    options_btn = Button(image=GEAR_TK, command= open_options, justify="center")
    options_btn.grid(column=5, row=1)

    refresh_file_selector()
    window.mainloop()
