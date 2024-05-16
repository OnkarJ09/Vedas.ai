from vedascli.plugins.audio import Vedas
import webbrowser


class Ytvdoplayer(Exception):
    pass


class Vedas:
    def __init__(self):
        pass

    def match_query(self, query):
        if "youtube" in query:
            return query.lower()

    def run(self, *args, **kwargs):
        query = self.match_query(kwargs["query"])
        if query:
            self.youtube_video_search(query)

    dependencies = ["audio"]

    def youtube_video_search(self, query):
        query = query.replace("search on youtube for", '')
        try:
            webbrowser.open(url=f'https://www.youtube.com/results?search_query={query}')
            Vedas.say(f"Trying to search {query} on youtube")
        except Ytvdoplayer:
            print("Sorry!! Please Try Again")
            Vedas.say("Sorry!! Please Try Again")
