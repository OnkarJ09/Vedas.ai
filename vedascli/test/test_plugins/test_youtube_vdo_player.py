import pytest

from vedascli.test.test_plugins.test_audio import test_say
import pywhatkit


@pytest.fixture(autouse=True)
def query():
    return "Vedas.ai"

def test_yt_vdo_player(query):
    test_say(f"Playing {query} on YouTube")
    pywhatkit.playonyt(query)
