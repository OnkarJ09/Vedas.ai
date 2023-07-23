import pyttsx3
import pytest


@pytest.fixture(autouse=True)
def audio():
    return "PRAGATI.ai"


def test_say(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.getProperty('rate')
    engine.setProperty('rate', 150)
    engine.say(audio)
    engine.runAndWait()
