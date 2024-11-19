import threading
import speech_recognition as sr
from gtts import gTTS
import requests
import asyncio
import fasttext
import os

# These are the languages and there respective codes accepted universally
languages = {
    "afrikaans": "af",
    "albanian": "sq",
    "amharic": "am",
    "arabic": "ar",
    "armenian": "hy",
    "assamese": "as",
    "aymara": "ay",
    "azerbaijani": "az",
    "bambara": "bm",
    "basque": "eu",
    "belarusian": "be",
    "bengali": "bn",
    "bhojpuri": "bho",
    "bosnian": "bs",
    "bulgarian": "bg",
    "catalan": "ca",
    "cebuano": "ceb",
    "chinese": "zh",
    "corsican": "co",
    "croatian": "hr",
    "czech": "cs",
    "danish": "da",
    "dhivehi": "dv",
    "dogri": "doi",
    "dutch": "nl",
    "english": "en",
    "esperanto": "eo",
    "estonian": "et",
    "ewe": "ee",
    "filipino (tagalog)": "fil",
    "finnish": "fi",
    "french": "fr",
    "frisian": "fy",
    "galician": "gl",
    "georgian": "ka",
    "german": "de",
    "greek": "el",
    "guarani": "gn",
    "gujarati": "gu",
    "haitian creole": "ht",
    "hausa": "ha",
    "hawaiian": "haw",
    "hebrew": "he",
    "hindi": "hi",
    "hmong": "hmn",
    "hungarian": "hu",
    "icelandic": "is",
    "igbo": "ig",
    "ilocano": "ilo",
    "indonesian": "id",
    "irish": "ga",
    "italian": "it",
    "japanese": "ja",
    "javanese": "jv",
    "kannada": "kn",
    "kazakh": "kk",
    "khmer": "km",
    "kinyarwanda": "rw",
    "konkani": "gom",
    "korean": "ko",
    "krio": "kri",
    "kurdish": "ku",
    "kurdish (sorani)": "ckb",
    "kyrgyz": "ky",
    "lao": "lo",
    "latin": "la",
    "latvian": "lv",
    "lingala": "ln",
    "lithuanian": "lt",
    "luganda": "lg",
    "luxembourgish": "lb",
    "macedonian": "mk",
    "maithili": "mai",
    "malagasy": "mg",
    "malay": "ms",
    "malayalam": "ml",
    "maltese": "mt",
    "maori": "mi",
    "marathi": "mr",
    "manipuri": "mni",
    "mizo": "lus",
    "mongolian": "mn",
    "myanmar (burmese)": "my",
    "nepali": "ne",
    "norwegian": "no",
    "nyanja": "ny",
    "odia": "or",
    "oromo": "om",
    "pashto": "ps",
    "persian": "fa",
    "polish": "pl",
    "portuguese (portugal, brazil)": "pt",
    "punjabi": "pa",
    "quechua": "qu",
    "romanian": "ro",
    "russian": "ru",
    "samoan": "sm",
    "sanskrit": "sa",
    "scots gaelic": "gd",
    "sepedi": "nso",
    "serbian": "sr",
    "sesotho": "st",
    "shona": "sn",
    "sindhi": "sd",
    "sinhala (sinhalese)": "si",
    "slovak": "sk",
    "slovenian": "sl",
    "somali": "so",
    "spanish": "es",
    "sundanese": "su",
    "swahili": "sw",
    "swedish": "sv",
    "tagalog (filipino)": "tl",
    "tajik": "tg",
    "tamil": "ta",
    "tatar": "tt",
    "telugu": "te",
    "thai": "th",
    "tigrinya": "ti",
    "tsonga": "ts",
    "turkish": "tr",
    "turkmen": "tk",
    "twi (akan)": "ak",
    "ukrainian": "uk",
    "urdu": "ur",
    "uyghur": "ug",
    "uzbek": "uz",
    "vietnamese": "vi",
    "welsh": "cy",
    "xhosa": "xh",
    "yiddish": "yi",
    "yoruba": "yo",
    "zulu": "zu"
}

class Vedas:
    pass


async def lang_detector(text):
    model = fasttext.load_model("lid.176.ftz")
    lang = model.predict(text, k=1)[0]
    return lang[0].replace("__label__", '')


async def say(text, language=None):
    """
                Converts text to speech and plays the audio.

                :param text: str, the text to be spoken
                :param language: str, the language code for the text-to-speech conversion
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
    tts_thread.join()  # Ensure thread completes execution before the continuation


# Asynchronous translation
async def translate_to_english(text, language):
    """
            Translates the given text to English if it's not already in English.

            :param text: str, the text to be translated
            :param language: str, the language code of the text
            :return: str, the translated text in English
            """
    if language != 'en':
        translation = await asyncio.to_thread(translator, text, 'en')
        return translation.lower()
    else:
        return text


# def translator_en(text, target_lang):
#         url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={text}"
#         response = requests.get(url=url)
#         translation = response.json()[0][0][0]
#         return translation


def translator(text, target_lang):
    """
            Translates text to the target language asynchronously using Google Translate API.

            :param text: str, the text to be translated
            :param target_lang: str, the target language code
            :return: str, translated text
            """
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={text}"
    response = requests.get(url=url)
    translation = response.json()[0][0][0]
    return translation


def detect_language_from_command(command):
    """
    Detects the new language from the command.

    :param command: str, the recognized command containing the language change request
    :return: str, the new language code if recognized, otherwise None
    """
    command = command.lower()
    for lang, code in languages.items():
        if lang.lower() in command.lower():
            return code
        return None


async def take_command(lang='en'):
    """
            Listens for a voice command from the user and returns the recognized text.
            By default, it listens in English (en) unless a change language command is received.

            :param lang: str, the language code to listen for (default is 'en')
            :return: str, the recognized text
            """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        await asyncio.to_thread(say, f"Listening in {lang.split}...", lang)
        recognizer.pause_threshold = 0.5
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google_cloud(audio, language=f"{lang}-US" if lang == 'en' else lang)
        await asyncio.to_thread(say, f"Recognized command: {query}", lang)
        query = await translate_to_english(query, language=lang)

        if "change language" in query.lower():
            new_lang = detect_language_from_command(query)
            if new_lang:
                await asyncio.to_thread(say, f"Changing language to {new_lang}", new_lang)
                return lang, True
            else:
                return query, False
    except sr.UnknownValueError:
        await asyncio.to_thread(say, "Sorry, I could not understand the audio.", lang)
        return None, False
    except sr.RequestError as e:
        await asyncio.to_thread(say, f"Could not request results; {e}", lang)
        return None, False

