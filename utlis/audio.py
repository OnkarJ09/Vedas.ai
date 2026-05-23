from manager.env_manager import DEFAULT_VOICE, DEFAULT_GENDER
from playsound import playsound
import edge_tts
import asyncio
from pathlib import Path
import fasttext
import pyaudio
import speech_recognition as sr
import json
from utlis.translator import translate
import os


# Define the base directory for output files
BASE_DIR = Path(__file__).resolve().parent.parent
FILES_DIR = str(BASE_DIR / "runtime")

# List of available languages
languages = {
  "afrikaans": "af",
  "albanian": "sq",
  "amharic": "am",
  "arabic": "ar",
  "azerbaijani": "az",
  "bengali": "bn",
  "bosnian": "bs",
  "bulgarian": "bg",
  "burmese": "my",
  "catalan": "ca",
  "chinese": "zh",
  "croatian": "hr",
  "czech": "cs",
  "danish": "da",
  "dutch": "nl",
  "english": "en",
  "estonian": "et",
  "filipino": "fil",
  "finnish": "fi",
  "french": "fr",
  "galician": "gl",
  "georgian": "ka",
  "german": "de",
  "greek": "el",
  "gujarati": "gu",
  "hebrew": "he",
  "hindi": "hi",
  "hungarian": "hu",
  "icelandic": "is",
  "indonesian": "id",
  "irish": "ga",
  "italian": "it",
  "japanese": "ja",
  "javanese": "jv",
  "kannada": "kn",
  "kazakh": "kk",
  "khmer": "km",
  "korean": "ko",
  "lao": "lo",
  "latvian": "lv",
  "lithuanian": "lt",
  "macedonian": "mk",
  "malay": "ms",
  "malayalam": "ml",
  "maltese": "mt",
  "marathi": "mr",
  "mongolian": "mn",
  "nepali": "ne",
  "norwegian": "nb",
  "pashto": "ps",
  "persian": "fa",
  "polish": "pl",
  "portuguese": "pt",
  "romanian": "ro",
  "russian": "ru",
  "serbian": "sr",
  "sinhala": "si",
  "slovak": "sk",
  "slovenian": "sl",
  "somali": "so",
  "spanish": "es",
  "swedish": "sv",
  "tamil": "ta",
  "telugu": "te",
  "thai": "th",
  "turkish": "tr",
  "ukrainian": "uk",
  "urdu": "ur",
  "uzbek": "uz",
  "vietnamese": "vi"
}


async def say(text, voice=DEFAULT_VOICE):
    """
        Say text to voice
    :param text:
    :param voice:
    :return: voice TTS
    """
    output_file = f"{FILES_DIR}/output.mp3"

    # Increase speed by 50% using the 'rate' parameter
    communicate = edge_tts.Communicate(text, voice, rate="+18%")

    await communicate.save(output_file)     # Save the output file

    playsound(output_file)  # Play the output file
    os.remove(output_file)

async def take_command(lang="en"):
    """
    Take command
    :param lang:
    :return: query
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("listening...")
        recognizer.pause_threshold = 0.5
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=None)

    try:
        query = recognizer.recognize_google(audio, language=lang)
        print("Recognized: " + str(query))

        # Always translate query to english for better results and matching
        query = query.lower()
        query = translate(text=query, target_language="en")
        print("[DEBUG] Translated Text: " + str(query))

        if "change language" in query:
            # Change recognization language
            new_lang = detect_code_from_language(query)

            # Change the voice like vise
            new_lang_voice = get_voices_by_language(query)
            print(f"[DEBUG] New language: {new_lang}")
            if not new_lang_voice:
                return query, False, [None, None]

            new_lang_voice = new_lang_voice[0]      # As for now hard coded to select first choice from list

            if new_lang and new_lang_voice:
                await say(f"changing language to {detect_language_from_code(new_lang)}")

            return query, True, [new_lang, new_lang_voice]
        return query, False, [None, None]

        return query

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None, False, [None, None]
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None, False, [None, None]



def get_voices_by_language(text):
    """
        Get voices by language
    :param text:
    :return: list of voices
    """

    text = text.lower()

    # Read the entire voice registry
    with open(f"{FILES_DIR}/vedas_voice_registry.json", "r") as f:
        voice_registry = json.load(f)

    # Check if any language name is present in the text
    for voice in voice_registry:
        if voice["language"].lower() in text:
            return [voice["voice_name"]]
    return []

def detect_code_from_language(text):
    """
        Detect language for the given text and return the corresponding language code
        It will be useful for changing the language in recognization
    :param text:
    :return:
    """
    text = text.lower()

    for lang, code in languages.items():
        if lang in languages:
            return code
    return "en"  # Default to English if no language is detected

def detect_language_from_code(text):
    text = text.lower()

    for lang, code in languages.items():
        if code in text:
            return lang
    return "english"


# TEST
if __name__ == "__main__":
    # say("नमस्कार, ही 'टेक्स्ट-टू-स्पीच' कार्यक्षमतेची चाचणी आहे. हे मोठ्याने बोलले जाणे अपेक्षित आहे.", lang="mr")
    # asyncio.run(say("Hello, this is a test of the text-to-speech functionality. This should be spoken at a higher speed."))
    while True:
      asyncio.run(take_command())