from .test_audio import test_say
import datetime


class Test_Vedas:
    def test___init__(self, **kwargs):
        self.keywords = ["morning", "afternoon", "evening", "night"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    def test_matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def test_run(self, *args, **kwargs):
        if self.last_query:
            hour = int(datetime.datetime.now().hour)
            if 0 <= hour < 12:
                test_say("Good morning")
                print("Good morning")
            elif 12 <= hour < 17:
                test_say("Good afternoon")
                print("Good afternoon")
            elif 17 <= hour < 20:
                test_say("Good evening")
                print("Good evening")
            else:
                test_say("Good night")
                print("Good night")

    dependencies = ["test_audio"]

