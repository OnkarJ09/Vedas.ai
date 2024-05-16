from vedascli.plugins.audio import Vedas
import wikipedia


class Vedas:
    def __init__(self):
        pass

    def match_query(self, query):
        q = {
            "wiki": self.wiki,
            "wikipedia": self.wiki
        }
        for i in q[0]:
            if i in query:
                return i[1]

    def run(self, *args, **kwargs):
        query = kwargs.get("query", '')
        query = query.replace("search wikipedia for", "")
        if query:
            return self.wiki(query)

    dependencies = ["audio"]

    @staticmethod
    def wiki(query):
        """
        Searches wikipedia for the given query and returns the first result.
        """
        results = wikipedia.search(query)
        if results:
            Vedas.say(wikipedia.summary(results, sentences=2))
        else:
            return "No results found."
