# Google's Unofficial Python API for Translation (faster)

from vedascli.data import lang_ids
from vedascli.utilities.lang_ids_for_recognizer import recognizer_lang_ids
import speech_recognition as sr
import requests
import pyttsx3
from gtts import gTTS
import os
import playsound
import langid
from textblob import TextBlob
from langdetect import detect
import fasttext


# def detect_lang(text):
#     model = fasttext.load_model('lid.176.ftz')
#     lang = model.predict(text, k=1)[0]
#     return str(lang[0].replace("__label__", ""))
lang_codec = recognizer_lang_ids()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        # lang_code = detect_lang(audio)
        #todo: Add here the langid para/ function to detect the language

        query = r.recognize_google(audio, language=lang_codec)
        # target_language = "en"
        # query = translator.translate_text(text_to_translate, target_language)
        print(f"User said: {query}\n")
        return query

    except Exception as e:
        print(e)
        print("Say that again please...")
        # return 'None'
    return 'None'


take_command()


def translate_text(text, target_language=lang_codec):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={text}"
    response = requests.get(url)
    translation = response.json()[0][0][0]
    return translation


def say(audio, lang=lang_codec):
    tts = gTTS(text=audio, lang=lang, slow=False)
    file_path = "output.mp3"
    tts.save(file_path)
    playsound.playsound(file_path)


translations = translate_text("नमस्ते")
# again_trans = translate_text(translations, "hi")
say(translations)
print(translations)
# print(detect_lang())
# say(detect_lang("olá, como vai você irmão, ram ram"))

# say("hello")
# Example usage
# text_to_translate = take_command()
# target_language = "fr"


# translated_text = translator.translate_text(take_command(), target_language)
# print(translated_text)
# print("Translated text:", text_to_translate)
