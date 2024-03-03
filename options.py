"""Py Replay Options

This script provides an options menu for configuring settings related to the Py Replay Actions application.
Users can set various options such as language, minimize behavior, and key assignments for stopping recording and playing.

Author: [Author Name]

"""

import json
import threading
from tkinter import *
from tkinter import END, ttk
import tkinter
from pynput import keyboard
from PIL import ImageTk, Image

from utils import FONT_NAME, YELLOW, languages, i18n, SCRIPT_DIR

# Default options configuration
default_options_config = {
    "language": 0,
    "minimize_when_play": 0,
    "minimize_when_record": 0,
    "stop_recording_key": "º",
    "stop_playing_key": "º",
}

options_config = {}

# Attempt to read options from config file, otherwise set defaults
try:
    readfile = open(f"{SCRIPT_DIR}/config.json", 'r')
    options_config = json.load(readfile)
except:
    with open(f"{SCRIPT_DIR}/config.json", 'w+') as readfile:
        json.dump(default_options_config, readfile)
    options_config = default_options_config
    
def get_i18n_literal(literal):
    """Get Internationalization Literal
    
    Retrieves the internationalized literal based on the current language configuration.

    Args:
        literal (str): The literal to retrieve.

    Returns:
        str: The internationalized literal.
    """
    try:
        return i18n[options_config['language']][literal]
    except:
        return "Error - literal not found"

def on_press_change_key(key, entry):
    """On Press Change Key
    
    Event handler for changing a key assignment.

    Args:
        key: The key pressed.
        entry (tkinter.Entry): The entry field to update with the new key.
    
    Returns:
        bool: False to stop the listener.
    """
    val = ""
    try:
        val = key.char
    except AttributeError:
        val = str(key).split(".")[-1]
    entry.config(state="normal")
    entry.delete(0,END)
    entry.insert(0,val)
    entry.config(state="readonly")
    
    return False

def update_entry_value(entry, value):
    """Update Entry Value
    
    Updates the value of a Tkinter Entry widget.

    Args:
        entry (tkinter.Entry): The entry field to update.
        value (str): The new value for the entry field.
    """
    entry.config(state="normal")
    entry.delete(0,END)
    entry.insert(0,value)
    entry.config(state="readonly")

def change_key(entry, root):
    """Change Key
    
    Opens a window to allow the user to change a key assignment.

    Args:
        entry (tkinter.Entry): The entry field to update with the new key.
        root (tkinter.Tk): The root Tkinter window.
    """
    tk_key_assignation = Toplevel(root)
    tk_key_assignation.title("")
    tk_key_assignation.config(padx=100, pady=50, bg=YELLOW)
    
    label = Label(tk_key_assignation, text=get_i18n_literal(literal="key_assignation_label"))
    label.grid(row=0, column=1, padx=10, pady=10)
    
    tk_key_assignation.grab_set()
    
    # Change key thread
    def change_key_thread(entry):
        keyboard_listener = keyboard.Listener(on_press=lambda event: on_press_change_key(event, entry))
        keyboard_listener.start()
        keyboard_listener.join()
        tk_key_assignation.destroy()
        
    thread = threading.Thread(target=lambda: change_key_thread(entry))
    thread.start()
    
def save_options(options_window, lang, minimize_record, minimize_play, record_key, play_key):
    """Save Options
    
    Saves the configured options to a JSON file.

    Args:
        options_window (tkinter.Toplevel): The options window.
        lang (int): The selected language index.
        minimize_record (tkinter.IntVar): The minimize record checkbox variable.
        minimize_play (tkinter.IntVar): The minimize play checkbox variable.
        record_key (str): The stop recording key.
        play_key (str): The stop playing key.
    """
    global options_config
    
    with open(f"{SCRIPT_DIR}/config.json", 'w+') as outfile:
        try:
            new_options_config = {
                "language": lang,
                "minimize_when_record": minimize_record.get(),
                "minimize_when_play": minimize_play.get(),
                "stop_recording_key": record_key,
                "stop_playing_key": play_key,
                }
            json.dump(new_options_config, outfile)
            options_config = new_options_config
            options_window.destroy()
        except Exception as e:
            print(e)

def open_options(root):
    """Open Options
    
    Opens the options menu for configuring settings.

    Args:
        root (tkinter.Tk): The root Tkinter window.
    """
    # Create a new window for the options menu
    options_window = Toplevel(root)
    options_window.title(get_i18n_literal(literal="options"))
    options_window.config(padx=10, pady=5, bg=YELLOW)

    # Combobox language select
    combo_label = Label(options_window, text=get_i18n_literal(literal="lang_label"))
    combo_label.grid(row=1, column=0, padx=10, pady=5)
    
    combo_lang = ttk.Combobox(options_window, values=languages['names'])
    combo_lang.grid(row=1, column=2, padx=10, pady=5)
    combo_lang.current(options_config["language"])
    
    # Minimize on play event checkbox
    minimize_when_play_label = Label(options_window, text=get_i18n_literal(literal="minimize_when_play_label"))
    minimize_when_play_label.grid(row=3, column=0, padx=10, pady=5)
    
    minimize_p_flag = tkinter.IntVar()
    minimize_when_play = ttk.Checkbutton(options_window, variable=minimize_p_flag)
    minimize_when_play.grid(row=3, column=2, padx=10, pady=5)
    # updating value from config
    minimize_p_flag.set(options_config['minimize_when_play'])
    
    # Minimize on record event checkbox
    
    minimize_when_record_label = Label(options_window, text=get_i18n_literal(literal="minimize_when_record_label"))
    minimize_when_record_label.grid(row=4, column=0, padx=10, pady=5)
    
    minimize_r_flag = tkinter.IntVar()
    minimize_when_record = ttk.Checkbutton(options_window, variable=minimize_r_flag)
    minimize_when_record.grid(row=4, column=2, padx=10, pady=5)
    # updating value from config
    minimize_r_flag.set(options_config['minimize_when_record'])
    
    # Stop record key assignation
    minimize_when_record_label = Label(options_window, text=get_i18n_literal(literal="stop_recording_key_label"))
    minimize_when_record_label.grid(row=5, column=0, padx=10, pady=5)
    
    stop_record_key = Entry(options_window, state="readonly", width=5, font=(FONT_NAME, 15, 'normal'),  justify="center")
    stop_record_key.bind("<1>", lambda event: change_key(stop_record_key, options_window))
    stop_record_key.grid(row=5, column=2, padx=10, pady=5)
    # Update value of entry
    update_entry_value(stop_record_key, options_config['stop_recording_key'])
    
    # Stop play key assignation
    
    minimize_when_play_label = Label(options_window, text=get_i18n_literal(literal="stop_playing_key_label"))
    minimize_when_play_label.grid(row=6, column=0, padx=10, pady=5)
    
    stop_play_key = Entry(options_window, state="readonly", width=5, font=(FONT_NAME, 15, 'normal'),  justify="center")
    stop_play_key.bind("<1>", lambda event: change_key(stop_play_key, options_window))
    stop_play_key.grid(row=6, column=2, padx=10, pady=5)
    # Update value of entry
    update_entry_value(stop_play_key, options_config['stop_playing_key'])
    
    SAVE_IMG = Image.open(f"{SCRIPT_DIR}/img/disk.png").resize((50,50), Image.LANCZOS)
    SAVE_TK = ImageTk.PhotoImage(SAVE_IMG)
    
    apply_btn = Button(options_window, image=SAVE_TK, command=lambda: save_options(options_window, combo_lang.current(), minimize_r_flag, minimize_p_flag, stop_record_key.get(), stop_play_key.get()))
    apply_btn.image = SAVE_TK  # This line is crucial to prevent garbage collection
    apply_btn.grid(row=7, column=1)

    # Make the options menu modal
    options_window.grab_set()
