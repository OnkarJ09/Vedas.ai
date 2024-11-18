import threading
import speech_recognition as sr
from gtts import gTTS
import requests
import asyncio
import fasttext
import os

# These are the languages and their respective codes accepted universally
languages = {
    "afrikaans": "af",
    "albanian": "sq",
    # ... [Other languages]
    "english": "en",
    "spanish": "es",
    # Add other languages as necessary
}

async def lang_detector(text):
    model = fasttext.load_model("lid.176.ftz")
    lang = model.predict(text, k=1)[0]
    return lang[0].replace("__label__", '')

async def say(text, language=None):
    """
    Converts text to speech and plays the audio.
    """
    def _say():
        if not language:
            detected_lang = lang_detector(text=text)
            lang_code = detected_lang if detected_lang in languages else 'en'
        else:
            lang_code = language

        tts = gTTS(text=text, lang=lang_code, slow=False)
        audio_file = "response.mp3"
        tts.save(audio_file)
        os.system("mpg123 " + audio_file)
        os.remove(audio_file)

    tts_thread = threading.Thread(target=_say)
    tts_thread.start()
    tts_thread.join()

async def translate_to_english(text, language):
    if language != 'en':
        translation = await asyncio.to_thread(translator, text, 'en')
        return translation.lower()
    else:
        return text

def translator(text, target_lang):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={text}"
    response = requests.get(url=url)
    translation = response.json()[0][0][0]
    return translation

def detect_language_from_command(command):
    command = command.lower()
    for lang, code in languages.items():
        if lang.lower() in command.lower():
            return code
    return None

async def take_command(lang='en'):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        await say(f"Listening in {lang}...", lang)
        recognizer.pause_threshold = 0.5
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google_cloud(audio, language=f"{lang}-US" if lang == 'en' else lang)
        await say(f"Recognized command: {query}", lang)
        query = await translate_to_english(query, language=lang)

        if "change language" in query.lower():
            new_lang = detect_language_from_command(query)
            if new_lang:
                await say(f"Changing language to {new_lang}", new_lang)
                return lang, True
            else:
                return query, False
    except sr.UnknownValueError:
        await say("Sorry, I could not understand the audio.", lang)
        return None, False
    except sr.RequestError as e:
        await say(f"Could not request results; {e}", lang)
        return None, False