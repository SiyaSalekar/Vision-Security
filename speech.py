import pyttsx3
import speech_recognition

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.runAndWait()

def speak(str):
    engine.say(str)
    engine.runAndWait()
speak("Hello, Please Tell your Student Email ID and Name")



recognizer = speech_recognition.Recognizer()
with speech_recognition.Microphone() as source:
    print("Say something")
    audio = recognizer.listen(source)

print("You said")
print(recognizer.recognize_google(audio))
print('Sorry.. run again...')