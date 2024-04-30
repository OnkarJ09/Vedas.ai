from vedascli.test.test_plugins.test_audio import test_say
import wikipedia


def test_wiki(query):
    """
    Searches wikipedia for the given query and returns the first result.
    """
    results = wikipedia.search(query)
    if results:
        test_say(wikipedia.summary(results, sentences=2))
    else:
        return "No results found."
