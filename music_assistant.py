import speech_recognition as sr
import pyttsx3
import pywhatkit
import random
import threading
import time

# Initialize recognizer and TTS
listener = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def talk(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source, duration=1)
            audio = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(audio)
            print(f"User: {command}")
            return command.lower()
    except:
        return ""

# Mood-based playlists
mood_playlists = {
    # Mood-based playlists (all instrumental)

    "happy": [
        "Upbeat instrumental jazz",
        "Acoustic guitar instrumental",
        "Energetic instrumental music"
    ],
    "sad": [
        "Sad piano instrumental",
        "Emotional violin instrumental",
        "Soft orchestral instrumental"
    ],
    "study": [
        "Lo-fi beats instrumental",
        "Calm piano instrumental",
        "Classical instrumental for focus"
    ]


}


def run_assistant():
    talk("Hello! Tell me your mood. Say happy, sad, or study.")
    mood = take_command()


    found_mood = None
    for key in mood_playlists.keys():
        if key in mood:   # partial match works
            found_mood = key
            break

    if found_mood:
        song = random.choice(mood_playlists[found_mood])
        talk(f"Playing a {found_mood} song: {song}")
        pywhatkit.playonyt(song)

   
       
    else:
        talk("Sorry, I didn't catch your mood clearly. Please say happy, sad, or study.")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    run_assistant()
