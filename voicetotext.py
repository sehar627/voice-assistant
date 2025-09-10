import speech_recognition as sr
import pyttsx3
import datetime

# -----------------------------
# Setup
# -----------------------------
recognizer = sr.Recognizer()
engine = pyttsx3.init()
running = True
notes = ""

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            command = command.lower()
            print(f"You said: {command}")
            return command
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError:
        print("Request failed; check your connection")
        return ""
# -----------------------------
# Voice Command Processing
# -----------------------------
def process_command(text):
    global notes
    text = text.lower()
    
    if "new line" in text:
        notes += "\n"
    elif "clear note" in text:
        notes = ""
    elif "delete last line" in text:
        lines = notes.strip().split("\n")
        notes = "\n".join(lines[:-1])
       
    elif "insert date" in text:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        notes += f"{now}\n"
       
    elif "save note" in text:
        with open("notes.txt", "w") as f:
            f.write(notes)
        
    elif "read note" in text:
        speak(notes)
    
    else:
        notes += text + " "

# -----------------------------
# Main Dictation Loop
# -----------------------------
print("Speech-to-Text Notepad started. Speak your commands or text.")


while running:
        command = take_command()
        if command:
            if "stop dictation" in command:
                running = False
                print("Final Notes:\n", notes)
            else:
                process_command(command)

