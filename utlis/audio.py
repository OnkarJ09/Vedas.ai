from manager.env_manager import DEFAULT_VOICE
try:
    from playsound3 import playsound
except ImportError:
    from playsound import playsound
import edge_tts
import asyncio
from pathlib import Path
from ctypes import CFUNCTYPE, c_char_p, c_int, cdll

# Suppress ALSA C library stderr warnings on Linux
try:
    _asound = cdll.LoadLibrary('libasound.so.2')
    _c_handler = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)(lambda *_: None)
    _asound.snd_lib_error_set_handler(_c_handler)
except Exception:
    pass

import pyaudio
import speech_recognition as sr
import time
import collections
import re
from utlis.vad import VadDetector
from utlis.kws import KeywordSpotterDetector

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




_kws_detector = None
_vad_detector = None


def get_kws_detector():
    global _kws_detector
    if _kws_detector is None:
        _kws_detector = KeywordSpotterDetector()
    _kws_detector.reset()
    return _kws_detector


def get_vad_detector():
    global _vad_detector
    if _vad_detector is None:
        _vad_detector = VadDetector()
    _vad_detector.reset()
    return _vad_detector


async def say(text, voice=DEFAULT_VOICE, lang="en", allow_interrupt=True):
    """
    Synthesize and play speech.
    If allow_interrupt is True, monitors the microphone via real-time offline KeywordSpotter (Sherpa-ONNX).
    Interrupts playback immediately (<10ms) if an offline trigger keyword ('WAIT', 'STOP', 'VEDAS', etc.) is heard.
    Returns:
        str: Recognized speech if interrupted with a new command.
        None: If playback completed without interruption, or if user just said 'stop'.
    """
    output_file = OUTPUT_FILES_DIR + "/output.mp3"

    communicate = edge_tts.Communicate(text, voice, rate="+18%")
    await communicate.save(output_file)

    if not allow_interrupt:
        playsound(output_file, block=True)
        return None

    # Open microphone stream for live offline keyword barge-in
    try:
        kws = get_kws_detector()
        vad = get_vad_detector()
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=512
        )
    except Exception as e:
        print(f"[Audio Warning] Could not initialize offline barge-in: {e}")
        playsound(output_file, block=True)
        return None

    sound = playsound(output_file, block=False)
    interrupted = False
    interrupted_keyword = None
    interrupted_frames = []
    pre_roll = collections.deque(maxlen=6)  # ~192ms pre-roll buffer

    start_time = time.time()
    grace_period = 0.20  # Grace period during audio startup

    try:
        while sound.is_alive():
            try:
                chunk = stream.read(512, exception_on_overflow=False)
                pre_roll.append(chunk)

                if time.time() - start_time < grace_period:
                    continue

                # Real-time offline keyword detection (<1ms per chunk on CPU)
                detected_kw = kws.detect(chunk)
                if detected_kw:
                    sound.stop()
                    interrupted = True
                    interrupted_keyword = detected_kw
                    print(f"\n[Vedas] Interrupted by keyword '{detected_kw}'!")
                    interrupted_frames = list(pre_roll)
                    break
            except Exception:
                continue

        # If playback completed naturally without interruption
        if not interrupted:
            sound.wait()
            return None

        # User interrupted: continue recording until natural silence
        silence_chunks = 0
        max_silence_chunks = int(1.2 / 0.032)  # ~1.2s silence threshold
        max_total_chunks = int(20.0 / 0.032)   # 20s phrase limit
        user_continued_speaking = False

        while silence_chunks < max_silence_chunks and len(interrupted_frames) < max_total_chunks:
            try:
                chunk = stream.read(512, exception_on_overflow=False)
                interrupted_frames.append(chunk)

                if vad.is_speech(chunk):
                    silence_chunks = 0
                    user_continued_speaking = True
                else:
                    silence_chunks += 1
            except Exception:
                break
    finally:
        try:
            stream.stop_stream()
            stream.close()
            p.terminate()
        except Exception:
            pass

    # Process interruption
    stop_words = {"stop", "pause", "cancel", "shut up", "be quiet", "quit"}
    if interrupted_keyword in ("STOP", "PAUSE", "CANCEL") and not user_continued_speaking:
        print("[Vedas] Playback stopped.")
        return None

    # Transcribe the interrupted user speech
    if interrupted_frames:
        recognizer = sr.Recognizer()
        raw_audio = b"".join(interrupted_frames)
        audio_data = sr.AudioData(raw_audio, 16000, 2)
        try:
            query = recognizer.recognize_google(audio_data, language=lang).strip()
            # If the user only said the stop keyword, do not treat it as a command
            if query.lower() in stop_words or not query:
                print("[Vedas] Playback stopped.")
                return None

            # Clean trigger prefix from follow-up command
            cleaned_query = re.sub(r"^(wait|stop|vedas|hold on|pause|listen|cancel)[,\s]*", "", query, flags=re.I).strip()
            result_query = cleaned_query if cleaned_query else query
            print(f"Recognized: {result_query}")
            return result_query
        except sr.UnknownValueError:
            if interrupted_keyword in ("STOP", "PAUSE", "CANCEL"):
                print("[Vedas] Playback stopped.")
            else:
                print("[Vedas] Interrupted. Listening for next command...")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

    return None

async def take_command(lang="en"):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("listening...")
        # shortcut: 1.8s pause threshold accommodates natural pauses/thinking; 0.8s non-speaking keeps mid-speech gaps
        recognizer.pause_threshold = 1.8
        recognizer.non_speaking_duration = 0.8
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=30)
        except sr.WaitTimeoutError:
            return ""

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