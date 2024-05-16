from vedascli.plugins.audio import Vedas
import pywhatkit


class Vedas:
    def __init__(self):
        pass

    def match_query(self, query):
        if "play" and "youtube" in query:
            return query.lower()

    def run(self, *args, **kwargs):
        query = self.match_query(kwargs["query"])
        if query:
            self.yt_vdo_player(query)

    dependencies = ["audio"]

    def yt_vdo_player(self, query):
        query = query.replace("play", '')
        query = query.replace("youtube", '')
        pywhatkit.playonyt(query)
        Vedas.say(f"Playing {query}")
        print(f"Playing {query}")
