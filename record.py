"""Py Replay Recorder

This script facilitates the recording of user events, such as keyboard presses, mouse clicks, movements, and scrolls,
for replaying them later. It utilizes Tkinter for the GUI, the pynput library for event monitoring, and other modules
for various functionalities.

Author: [Author Name]

"""

import json
from tkinter import *
import time
import threading

from pynput import keyboard, mouse
import logging
from floating_message import FloatingMessage

import options
from utils import SCRIPT_DIR


# ---------------------------- CONSTANTS ------------------------------- # 

events = []
recording = False

# ---------------------------- FUNCTIONS ------------------------------- # 

def get_duration_event():
    """Get Duration of Event
    
    Calculates the duration of the last event.

    Returns:
        float: The duration of the event.
    """
    if len(events) == 0:
        return 0
    return time.time() - events[-1]['time']

def minimize_window(window):
    """Minimize Window
    
    Minimizes the application window.

    Args:
        window (tkinter.Tk): The Tkinter window to minimize.
    """
    window.iconify()

def maximize_window(window):
    """Maximize Window
    
    Maximizes the application window.

    Args:
        window (tkinter.Tk): The Tkinter window to maximize.
    """
    window.deiconify()

def on_press(key, mouse_listener):
    """On Press
    
    Event handler for key press events.

    Args:
        key: The key pressed.
    """
    global recording
    
    if recording is not True:
        logging.info("finishing keyboard thread recording")
        mouse_listener.stop()
        return False
    try:
        logging.info(f"pressing-{key}")
        # check to finish keyboard listener (detect button configured as 'stop_recording_key')
        if hasattr(key, "char") and key.char is not None:
            if key.char == options.options_config["stop_recording_key"]:
                recording = False
                mouse_listener.stop()
                return False
            json_object = {'action':'pressed_key', 'key':key.char, 'time': time.time(), 'duration': get_duration_event()}
        elif hasattr(key, "name"):
            json_object = {'action':'pressed_key', 'key':key.name, 'time': time.time(), 'duration': get_duration_event()}
        elif hasattr(key, "vk"):
            json_object = {'action':'pressed_key', 'vk':key.vk, 'time': time.time(), 'duration': get_duration_event()}
    except AttributeError:
        json_object = {'action':'pressed_key', 'key':str(key).split(".")[-1], 'time': time.time(), 'duration': get_duration_event()}
    events.append(json_object)
    

def on_release(key):
    """On Release
    
    Event handler for key release events.

    Args:
        key: The key released.
    """
    global recording
    
    if recording is not True:
        return False
    try:
        logging.info(f"release-{key}")
        if hasattr(key, "char") and key.char is not None:
            json_object = {'action':'released_key', 'key':key.char, 'time': time.time(), 'duration': get_duration_event()}
        elif hasattr(key, "name"):
            json_object = {'action':'released_key', 'key':key.name, 'time': time.time(), 'duration': get_duration_event()}
        elif hasattr(key, "vk"):
            json_object = {'action':'released_key', 'vk':key.vk, 'time': time.time(), 'duration': get_duration_event()}
    except AttributeError:
        json_object = {'action':'released_key', 'key':str(key).split(".")[-1], 'time': time.time(), 'duration': get_duration_event()}
    events.append(json_object)
        

def on_move(x, y):
    """On Move
    
    Event handler for mouse movement events.

    Args:
        x (int): The x-coordinate of the mouse.
        y (int): The y-coordinate of the mouse.
    """
    global recording
    
    if recording is not True:
        return False
    if len(events) >= 1:
        logging.info(f"moving mouse to [{x}-{y}]")
        if events[-1]['action'] != "moved":
            json_object = {'action':'moved', 'x':x, 'y':y, 'time':time.time(), 'duration': get_duration_event()}
            events.append(json_object)
        elif events[-1]['action'] == "moved" and time.time() - events[-1]['time'] > 0.05:
            json_object = {'action':'moved', 'x':x, 'y':y, 'time':time.time(), 'duration': get_duration_event()}
            events.append(json_object)
    else:
        json_object = {'action':'moved', 'x':x, 'y':y, 'time':time.time(), 'duration': get_duration_event()}
        events.append(json_object)


def on_click(x, y, button, pressed):
    """On Click
    
    Event handler for mouse click events.

    Args:
        x (int): The x-coordinate of the mouse.
        y (int): The y-coordinate of the mouse.
        button: The mouse button clicked.
        pressed (bool): Whether the button was pressed or released.
    """
    global recording
    
    if recording is not True:
        return False
    logging.info(f"click on [{x}-{y}]")
    json_object = {'action':'pressed_mouse' if pressed else 'released_mouse', 'button':str(button).split(".")[-1], 'x':x, 'y':y, 'time':time.time(), 'duration': get_duration_event()}
    events.append(json_object)


def on_scroll(x, y, dx, dy):
    """On Scroll
    
    Event handler for mouse scroll events.

    Args:
        x (int): The x-coordinate of the mouse.
        y (int): The y-coordinate of the mouse.
        dx (int): The horizontal scroll amount.
        dy (int): The vertical scroll amount.
    """
    global recording
    
    if recording is not True:
        return False
    logging.info(f"scrolling to [{x}-{y}]")
    json_object = {'action': 'scroll', 'vertical_direction': int(dy), 'horizontal_direction': int(dx), 'x':x, 'y':y, 'time': time.time(), 'duration': get_duration_event()}
    events.append(json_object)


def record_events():
    """Record Events
    
    Records user events such as keyboard presses, mouse clicks, movements, and scrolls.

    Returns:
        list: A list of recorded events.
    """
    global recording, events
    
    if recording is True:
        return
    
    logging.info("Starting listeners:")
    
    # Declare listeners
    recording = True
    events = []

    mouse_listener = mouse.Listener(
        on_click=on_click,
        on_scroll=on_scroll,
        on_move=on_move)
    
    keyboard_listener = keyboard.Listener(
        on_press=lambda event: on_press(event, mouse_listener),
        on_release=on_release)

    # starting keylogger threads
    keyboard_listener.start()
    mouse_listener.start()
    
    # joining keylogger threads into main thread
    keyboard_listener.join()
    mouse_listener.join()

    logging.info("Finishing listeners")
    
    return events
    
    
def start_record_events_thread(btns, window, refresh_file_selector):
    """Start Record Events Thread
    
    Initiates a thread for recording events.

    Args:
        record_btn (tkinter.Button): The button to initiate recording.
        window (tkinter.Tk): The Tkinter window.
        refresh_file_selector (function): The function to refresh file selectors.
    """
    
    #disable required buttons of GUI
    for btn in btns:
        btn.config(state="disabled")
    
    #Show tooltip to remember stop button at top left
    stop_record_message = options.get_i18n_literal("stop_recording_message")
    floating_message = FloatingMessage(window, stop_record_message.replace("@", options.options_config["stop_recording_key"]))
    floating_message.show()
    
    if window != None and options.options_config["minimize_when_record"] == 1:
        minimize_window(window)
        
    
    # Define the function that will run in the thread
    def thread_function():
        from tkinter import filedialog
        
        final_events = record_events()
        
        # check to finish mouse listener (detect release of button right)
        if len(final_events) > 1:
            directory = filedialog.asksaveasfilename(initialdir=f"{SCRIPT_DIR}/data", initialfile="record.json", defaultextension=".json", filetypes=(("record file", "*.json"),("All Files", "*.*") ))
            logging.info(directory)
            if directory is not None and directory != "":
                with open(directory, 'w+') as outfile:
                    json.dump(events, outfile)
                refresh_file_selector()

        #enable required buttons of GUI
        def reenable_btns(btns):
            for btn in btns:
                btn.config(state="active")
        
        # Modify the button after the task is completed
        if window != None:
            window.after(0, lambda: reenable_btns(btns))
            maximize_window(window)
            
        floating_message.hide()
    
    # Create a new thread
    thread = threading.Thread(target=thread_function)
    # Start the thread
    thread.start()