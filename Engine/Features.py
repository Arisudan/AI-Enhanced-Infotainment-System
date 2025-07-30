import os
from playsound import playsound
import eel
from Engine.command import speak
from Engine.config import ASSISTANT_NAME

#Playing Assistant Sound
@eel.expose
def playAssistantSound():
    music_dir = "www/assets/Audio/start_sound.mp3"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()


    if query:
        speak("Opening "+query)
        os.system('start '+query)
    else:
        speak("Not found")
