from project.features.audio import say
import wikipedia


def wiki(query):
    """
    Searches wikipedia for the given query and returns the first result.
    """
    results = wikipedia.search(query)
    if results:
        say(wikipedia.summary(results, sentences=2))
    else:
        return "No results found."
