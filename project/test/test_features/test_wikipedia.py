from project.test.test_features.test_audio import test_say
import wikipedia
import pytest


@pytest.fixture(autouse=True)
def query():
    return "Vedas.ai"


@pytest.fixture(autouse=True)
def audio():
    return "Vedas.ai"


def test_wiki(query):
    """
    Searches wikipedia for the given query and returns the first result.
    """
    results = wikipedia.search(query)
    if results:
        test_say(wikipedia.summary(results, sentences=2))
    else:
        return "No results found."
