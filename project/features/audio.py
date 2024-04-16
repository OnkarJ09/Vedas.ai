import pyttsx3


def say(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.getProperty('rate')
    engine.setProperty('rate', 150)
    engine.say(audio)
    engine.runAndWait()
