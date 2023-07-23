import pytest

from test.test_features.test_audio import test_say
import pywhatkit


@pytest.fixture(autouse=True)
def query():
    return "PRAGATI.ai"

def test_yt_vdo_player(query):
    test_say(f"Playing {query} on YouTube")
    pywhatkit.playonyt(query)

