"""Py Replay Player

This script facilitates the replaying of recorded user events, such as keyboard presses, mouse clicks, movements, and scrolls.
It utilizes Tkinter for the GUI, the pynput library for event monitoring, and other modules for various functionalities.

Author: [Author Name]

"""

import json
from tkinter import *
import time
import threading

from pynput import keyboard
import logging
from floating_message import FloatingMessage

import options
from utils import SCRIPT_DIR


# ---------------------------- CONSTANTS ------------------------------- # 

playing = False
looping = False
looping_check = False

# ---------------------------- FUNCTIONS ------------------------------- # 


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

def on_press_replay(key):
    """On Press Replay
    
    Event handler for key press events during replay.

    Args:
        key: The key pressed.
    """
    global playing, looping
    
    logging.info(f"replay-pressing-{key}")
    
    # check to finish keyboard listener (detect button configured key as 'stop_playing_key')
    if hasattr(key, 'char') and key.char == options.options_config["stop_playing_key"]:
        logging.info(f"Finishing replay manually")
        playing = False
        looping = False
        return False

def start_replay_events_thread(btns, file, window, looping_check):
    """Start Replay Events Thread
    
    Initiates a thread for replaying recorded events.

    Args:
        play_btn (tkinter.Button): The button to initiate replay.
        file (str): The name of the file containing recorded events.
        window (tkinter.Tk): The Tkinter window.
        looping_check (bool): Whether to loop the replay or not.
    """
    global playing, looping
    
    #disable required buttons of GUI
    for btn in btns:
        btn.config(state="disabled")
        
    playing = True
    
    #Show tooltip to remember stop button at top left
    stop_record_message = options.get_i18n_literal("stop_playing_message")
    floating_message = FloatingMessage(window, stop_record_message.replace("@", options.options_config["stop_playing_key"]))
    floating_message.show()
    
    if window != None and options.options_config["minimize_when_play"] == 1:
        minimize_window(window)
    
    # Define the function that will run in the thread
    def replay_thread_function(file, looping_check):
        global looping
        
        import json
        import time
        from pynput.keyboard import Key, Controller as KeyboardController, KeyCode
        from pynput.mouse import Button, Controller as MouseController
            
        looping = False
        
        if looping_check is True:
            looping = True
        
        replay(KeyboardController, MouseController, Button, Key, file, KeyCode)
        
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
    replay_thread = threading.Thread(target=lambda: replay_thread_function(file, looping_check))
    # Start the thread
    replay_thread.start()
    
def replay(KeyboardController, MouseController, Button, Key, file, KeyCode):
    """Replay
    
    Replays recorded events.

    Args:
        KeyboardController: The keyboard controller from pynput.
        MouseController: The mouse controller from pynput.
        Button: The mouse button from pynput.
        Key: The keyboard key from pynput.
        file (str): The name of the file containing recorded events.
    """
    # Define the function that will run in the thread
    
    keyboard_listener = keyboard.Listener(on_press=on_press_replay)
    keyboard_listener.start()
    
    replay_events(KeyboardController, MouseController, Button, Key, file, KeyCode)
    # Stop keyboard thread
    
    if keyboard_listener.is_alive():
        keyboard_listener.stop()

def replay_events(KeyboardController, MouseController, Button, Key, file, KeyCode):
    """Replay Events
    
    Replays recorded events.

    Args:
        KeyboardController: The keyboard controller from pynput.
        MouseController: The mouse controller from pynput.
        Button: The mouse button from pynput.
        Key: The keyboard key from pynput.
        file (str): The name of the file containing recorded events.
    """
    global playing, looping
    
    name_of_recording = file
    
    logging.info(name_of_recording)
    looping_counter = 1
    
    while looping_counter > 0:
        # Read events from file
        f = open(SCRIPT_DIR + f"/data/{name_of_recording}", 'r')
        json_file = json.load(f)
        
        keyboard = KeyboardController()
        mouse = MouseController()

        for json_line in json_file:
            # logging.info(json_line)
            
            if playing is not True:
                break
            
            time.sleep(json_line['duration'])
            
            if json_line['action'] == 'pressed_key':
                if "key" in json_line and hasattr(Key, json_line['key']):
                    keyboard.press(Key[json_line['key']])
                elif "vk" in json_line:
                    keyboard.press(KeyCode.from_vk(json_line['vk']))
                else:
                    keyboard.press(json_line['key'])
                
            elif json_line['action'] == 'released_key':
                if "key" in json_line and hasattr(Key, json_line['key']):
                    keyboard.release(Key[json_line['key']])
                elif "vk" in json_line:
                    keyboard.release(KeyCode.from_vk(json_line['vk']))
                else:
                    keyboard.release(json_line['key'])
            
            elif json_line['action'] == 'moved':
                mouse.position = (json_line['x'], json_line['y'])  
            
            elif json_line['action'] == 'pressed_mouse':
                mouse.press(Button[json_line['button']]) 
                
            elif json_line['action'] == 'released_mouse':
                mouse.release(Button[json_line['button']])  
                
            elif json_line['action'] == 'scroll':
                mouse.scroll(json_line['button'], json_line['y'])  
        
        if looping is not True:
            looping_counter -= 1
    
    
    logging.info(f"{name_of_recording} - finished!")
    playing = False
