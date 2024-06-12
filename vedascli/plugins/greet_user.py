from .audio import say
import datetime


class Vedas:
    def __init__(self, **kwargs):
        self.keywords = ["morning", "afternoon", "evening", "night"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    def matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def run(self, *args, **kwargs):
        if self.last_query:
            hour = int(datetime.datetime.now().hour)
            if 0 <= hour < 12:
                say("Good morning")
                print("Good morning")
            elif 12 <= hour < 17:
                say("Good afternoon")
                print("Good afternoon")
            elif 17 <= hour < 20:
                say("Good evening")
                print("Good evening")
            else:
                say("Good night")
                print("Good night")

    dependencies = ["audio"]

