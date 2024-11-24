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
                print("Good morning")
                return "Good morning"
            elif 12 <= hour < 17:
                print("Good afternoon")
                return "Good afternoon"
            elif 17 <= hour < 20:
                print("Good evening")
                return "Good evening"
            else:
                print("Good night")
                return "Good night"
