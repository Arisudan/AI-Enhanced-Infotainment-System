import os
from playsound import playsound
import eel
from Engine.config import ASSISTANT_NAME
   
@eel.expose
def playAssistantSound():
    music_dir = os.path.abspath("www/assets/Audio/start_sound.mp3")
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    if query!="":
        speak("Opening "+query)
        os.system('start '+query)
    else:
        speak("Not found")
