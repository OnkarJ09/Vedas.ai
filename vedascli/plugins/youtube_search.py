from vedascli.plugins.audio import Plugin
import webbrowser


class Ytvdoplayer(Exception):
    pass


class Plugin:
    def __init__(self):
        pass

    def match_query(self, query):
        if "youtube" in query:
            return query.lower()

    def run(self, *args, **kwargs):
        query = self.match_query(kwargs["query"])
        if query:
            self.youtube_video_search(query)

    def youtube_video_search(self, query):
        query = query.replace("search on youtube for", '')
        try:
            webbrowser.open(url=f'https://www.youtube.com/results?search_query={query}')
            Plugin.say(f"Trying to search {query} on youtube")
        except Ytvdoplayer:
            print("Sorry!! Please Try Again")
            Plugin.say("Sorry!! Please Try Again")
