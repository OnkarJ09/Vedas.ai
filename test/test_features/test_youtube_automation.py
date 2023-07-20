import pytest
import pywhatkit


@pytest.fixture(autouse=True)
def query():
    return "test"

class TestYoutubefailed(Exception):
    pass


def test_youtube_auto(query):
    try:
        pywhatkit.playonyt(query)
    except TestYoutubefailed:
        pytest.fail("Exception raised and not able to search on youtube")
