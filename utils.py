import os
import sys

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

languages = {
    "names": ["English", "Español"],
    "langs": ["en", "es"]
}

""" 
I18N: 
0 - en
1 - es
"""
i18n = [
    {
        "options": "Options",
        "lang_label": "Language:",
        "minimize_when_play_label": "Minimize when play record:",
        "minimize_when_record_label": "Minimize when start recording:",
        "stop_recording_key_label": "Stop recording key:",
        "stop_playing_key_label": "Stop playing key:",
        "key_assignation_label": "Press a key to assign",
        "confirm": "Are you sure?",
        "yes": "Are you sure?",
        "no": "Are you sure?",
        "delete": "Delete",
        "play": "Delete",
        "looping": "Delete",
        "options": "Options",
        "record": "Record",
        "stop_recording_message": "Stop recording by pressing @ Key",
        "stop_playing_message": "Stop playing by pressing @ Key",
    },
    {
        "options": "Opciones",
        "lang_label": "Idioma:",
        "minimize_when_play_label": "Minimizar al iniciar reproducción:",
        "minimize_when_record_label": "Minimizar al iniciar grabación:",
        "stop_recording_key_label": "Tecla para terminar grabación:",
        "stop_playing_key_label": "Tecla para terminar reproducción:",
        "key_assignation_label": "Pulsa una tecla para asignar",
        "confirm": "¿Estas seguro?",
        "yes": "¿Estas seguro?",
        "no": "¿Estas seguro?",
        "delete": "Borrar",
        "play": "Reproducir",
        "looping": "Bucle",
        "options": "Opciones",
        "record": "Grabar",
        "stop_recording_message": "Presiona @ para detener la captura de eventos",
        "stop_playing_message": "Presiona @ para detener la reproducción",
    }
]



# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
elif __file__:
    SCRIPT_DIR = os.path.dirname(__file__)

RESOURCES_DIR = os.path.dirname(__file__)