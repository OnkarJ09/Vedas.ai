import pytest
from unittest.mock import patch, MagicMock
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
    lang = model.predict(text, k=1)
    return lang[0][0]

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


# Test for lang_detector function
@patch('audio.fasttext.load_model')
def test_lang_detector(mock_load_model):
    # Create a mock model
    mock_model = MagicMock()
    mock_model.predict.return_value = (['__label__en'], [0.9])
    mock_load_model.return_value = mock_model

    result = asyncio.run(lang_detector("Hello"))

    # Extract the language code from the result
    language_code = result.split('__label__')[1] if '__label__' in result else None

    # Assert that the language code is 'en'
    assert language_code == "en"  # Expecting English language code

# Test for detect_language_from_command function
def test_detect_language_from_command():
    command = "Please speak in Spanish"
    result = detect_language_from_command(command)
    assert result == "es"  # Expecting Spanish language code

    command = "Hello"
    result = detect_language_from_command(command)
    assert result is None  # No language detected

# Test for translate_to_english function
@patch('audio.translator')
@pytest.mark.asyncio
async def test_translate_to_english(mock_translator):
    mock_translator.return_value = "Hello"

    result = await translate_to_english("Hola", "es")
    assert result == "hello"  # Expecting translated text in lower case

    result = await translate_to_english("Hello", "en")
    assert result == "Hello"  # Expecting the same text back

# Test for say function
@patch('audio.gTTS')
@patch('audio.os.system')
@pytest.mark.asyncio
async def test_say(mock_os_system, mock_gTTS):
    mock_gTTS.return_value.save = MagicMock()

    await say("Hello", "en")

    # Check if gTTS was called with the correct parameters
    mock_gTTS.assert_called_once_with(text="Hello", lang="en", slow=False)

    # Check if the audio file was saved
    mock_gTTS.return_value.save.assert_called_once_with("response.mp3")

    # Check if the audio file was played
    mock_os_system.assert_called_once_with("mpg123 response.mp3")

    # Check if the audio file was removed after playing
    assert not os.path.exists("response.mp3")

# Run the tests
if __name__ == "__main__":
    pytest.main()