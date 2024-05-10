import webbrowser
from .audio import say


def search_and_open(query):
    query = query.replace("search for", '')
    search_url = f"https://www.google.com/search?={query}"
    webbrowser.open(search_url)
    say(f"ok, searching for {query}")
