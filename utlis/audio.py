from manager.env_manager import DEFAULT_VOICE
from playsound import playsound
import edge_tts
import asyncio
from pathlib import Path
import fasttext
import pyaudio
import speech_recognition as sr

# Define the base directory for output files
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILES_DIR = str(BASE_DIR / "runtime")

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
    :return:
    """
    output_file = OUTPUT_FILES_DIR + "/output.mp3"

    # Increase speed by 50% using the 'rate' parameter
    communicate = edge_tts.Communicate(text, voice, rate="+18%")

    await communicate.save(output_file)     # Save the output file

    playsound(output_file)  # Play the output file

async def take_command(lang="en"):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("listening...")
        recognizer.pause_threshold = 0.5
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio, language=lang)
        print("Recognized: " + str(query))
        return query
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""



async def lang_detector(text):
    """
    Detect language
    :param text:
    :return: language code
    """

    # with open()
    pass
    # model = fasttext.load_model("lid.176.ftz")
    # lang = model.predict(text, k=1)[0]
    # return lang[0].replace("__label__", '')

# TEST
if __name__ == "__main__":
    # say("नमस्कार, ही 'टेक्स्ट-टू-स्पीच' कार्यक्षमतेची चाचणी आहे. हे मोठ्याने बोलले जाणे अपेक्षित आहे.", lang="mr")
    # asyncio.run(say("Hello, this is a test of the text-to-speech functionality. This should be spoken at a higher speed."))
    while True:
      asyncio.run(take_command())