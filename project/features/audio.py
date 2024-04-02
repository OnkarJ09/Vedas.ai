import pyttsx3
from mtranslate import translate


def say(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.getProperty('rate')
    engine.setProperty('rate', 150)
    # to_translate = audio
    # translate(to_translate, 'hi')
    engine.say(audio)
    engine.runAndWait()
