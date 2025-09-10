import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
import random
import time
import threading

# Initialize recognizer
listener = sr.Recognizer()

reminders = []

# ---------- NEW TALK FUNCTION ----------
def talk(text):
    print(f"Assistant: {text}")

    def speak():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    threading.Thread(target=speak, daemon=True).start()
# --------------------------------------

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"User: {command}")
    except:
        command = ""
    return command

# Thread to check reminders
def reminder_checker():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        for reminder in reminders:
            if reminder['time'] == now:
                talk(f"Reminder: {reminder['task']}")
                reminders.remove(reminder)
        time.sleep(30)  # check every 30 seconds

# Start reminder checker in background
threading.Thread(target=reminder_checker, daemon=True).start()

def run_assistant():
    command = take_command()

    if "hey assistant" in command:
        command = command.replace("hey assistant", "").strip()
        if not command:
            talk("Yes? How can I help you?")
            return

        # Play song
        if 'play' in command:
            song = command.replace('play', '')
            talk(f'Playing {song}')
            pywhatkit.playonyt(song)

        # Tell time
        elif 'time' in command:
            time_now = datetime.datetime.now().strftime('%I:%M %p')
            talk(f'The time is {time_now}')

        # Tell date
        elif 'date' in command:
            date_now = datetime.datetime.now().strftime('%A, %B %d, %Y')
            talk(f'Today is {date_now}')

        # Wikipedia search
        elif 'wikipedia' in command:
            person = command.replace('wikipedia', '')
            try:
                info = wikipedia.summary(person, sentences=2)
                talk(info)
            except:
                talk("Sorry, I couldn't find that on Wikipedia.")

        # Open website
        elif 'open' in command:
            site = command.replace('open', '').strip()
            url = f"https://{site}.com"
            webbrowser.open(url)
            talk(f'Opening {site}')

        # Google search
        elif 'search' in command:
            search_term = command.replace('search', '')
            pywhatkit.search(search_term)
            talk(f'Searching for {search_term}')

        # Tell joke
        elif 'joke' in command:
            jokes = [
                "Why did the computer show up at work late? It had a hard drive.",
                "Why don’t scientists trust atoms? Because they make up everything.",
                "Why did the smartphone need glasses? It lost its contacts."
            ]
            talk(random.choice(jokes))

        # Set reminder
        elif 'remind me to' in command:
            try:
                # Example command: "remind me to call mom at 18:30"
                task_part = command.replace('remind me to', '').strip()
                if 'at' in task_part:
                    task, reminder_time = task_part.split('at')
                    task = task.strip()
                    reminder_time = reminder_time.strip()
                    # Store reminder
                    reminders.append({'task': task, 'time': reminder_time})
                    talk(f'Reminder set for {task} at {reminder_time}')
                else:
                    talk("Please specify time like 'at 18:30'")
            except:
                talk("Sorry, I couldn't set that reminder.")

        # Default response
        else:
            talk("I didn't understand that. Can you repeat?")

# ----------------- MAIN LOOP -----------------
if __name__ == "__main__":
    talk("Hello, I am your Assistant. Say 'Hey Assistant' to start.")
    while True:
        run_assistant()