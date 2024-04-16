# Google's Unofficial Python API for Translation (faster then t1)


import speech_recognition as sr
import requests


def translate_text(text, target_language):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={text}"
    response = requests.get(url)
    translation = response.json()[0][0][0]
    return translation


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='hi')
        # target_language = "en"
        # query = translator.translate_text(text_to_translate, target_language)
        print(f"User said: {query}\n")
        return query
    except Exception as e:
        print(e)
        print("Say that again please...")
        # return 'None'
    return 'None'


translations = translate_text(take_command(), "en")
print(translations)
# Example usage
# text_to_translate = take_command()
# target_language = "fr"


# translated_text = translator.translate_text(take_command(), target_language)
# print(translated_text)
# print("Translated text:", text_to_translate)
