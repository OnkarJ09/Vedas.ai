from vedascli.plugins.translator import Vedas
import speech_recognition as sr
from gtts import gTTS
from vedascli.utilities import lang_detector
import requests
import os


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


def say(text, language=None):
    """
        Converts text to speech and plays the audio.

        :param text: str, the text to be spoken
        :param language: str, the language code for the text-to-speech conversion
        """
    if not language:
        detected_language = lang_detector.detect_lang(text)
        language = detected_language if detected_language in languages else 'en'
    tts = gTTS(text=text, lang=language, slow=False)
    audio_file = "response.mp3"
    tts.save(audio_file)
    os.system("mpg123 " + audio_file)
    os.remove(audio_file)

def translate_to_english(text, language):
    """
    Translates the given text to English if it's not already in English.

    :param text: str, the text to be translated
    :param language: str, the language code of the text
    :return: str, the translated text in English
    """
    if language != 'en':
        translator = Vedas.translate_text(text, 'en')
        translated_text = translator.lower()
        return translated_text
    else:
        return text


def translator(text, target_language):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={text}"
    response = requests.get(url)
    translation = response.json()[0][0][0]
    return translation

def take_command(language='en'):
    """
    Listens for a voice command from the user and returns the recognized text.
    By default, it listens in English (en) unless a change language command is received.

    :param language: str, the language code to listen for (default is 'en')
    :return: str, the recognized text
    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        say(f"Listening in {language}...", language)
        recognizer.pause_threshold = 0.5
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio, language=f"{language}-US" if language == 'en' else language)
        say(f"Recognized command: {query}", language)
        query = translate_to_english(query, language)

        if "change language" in query.lower():
            new_language = detect_language_from_command(query)
            if new_language:
                say(f"Changing language to {new_language}", new_language)
                return new_language, True
            else:
                say("Sorry, I couldn't recognize the new language.", language)
                return language, False
        else:
            return query, False

    except sr.UnknownValueError:
        say("Sorry, I could not understand the audio.", language)
        return None, False
    except sr.RequestError as e:
        say(f"Could not request results; {e}", language)
        return None, False


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


# if __name__ == "__main__":
#     # Default language is English
#     current_language = 'en'
#
#     while True:
#         command, language_changed = take_command(current_language)
#
#         if command is None:
#             continue  # Repeat listening if the command wasn't understood
#
#         if language_changed:
#             current_language = command
#             continue  # Skip further processing and start listening in new language
#
#         # Process the recognized command (in the current language)
#         # Your virtual assistant's existing command processing logic here
#         say(f"Processing command: {command} in language: {current_language}", current_language)
