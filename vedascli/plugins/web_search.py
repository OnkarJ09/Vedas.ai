from vedascli.plugins.audio import Vedas
import webbrowser


class Vedas:
    def __init__(self):
        pass

    def match_query(self, query):
        if "search for" in query:
            return query.lower()

    def run(self, *args, **kwargs):
        query = kwargs.get("query", '')
        if query:
            return self.search_and_open(query)

    dependencies = ["audio"]

    @staticmethod
    def search_and_open(query):
        query = query.replace("search for", '')
        search_url = f"https://www.google.com/search?={query}"
        webbrowser.open(search_url)
        Vedas.say(f"ok, searching for {query}")
