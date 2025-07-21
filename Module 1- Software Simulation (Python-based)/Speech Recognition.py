import speech_recognition as sr
import pyttsx3

# Initialize engines
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except:
            speak("Sorry, I didn't catch that.")
            return ""

# Main loop
while True:
    cmd = listen()
    if "play music" in cmd:
        speak("Playing your favorite track!")
    elif "navigate home" in cmd:
        speak("Opening navigation to home.")
    elif "exit" in cmd:
        speak("Goodbye!")
        break
