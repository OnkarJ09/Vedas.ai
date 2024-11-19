import pytest
import datetime
# from test_audio import test_say

class Vedas:
    def __init__(self):
        self.keywords = ["morning", "afternoon", "evening", "night"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    def matches_query(self, query):
        return any(keyword in query.lower() for keyword in self.keywords)

    def run(self, *args, **kwargs):
        if self.last_query:
            hour = int(datetime.datetime.now().hour)
            if 0 <= hour < 12:
                # test_say("Good morning")
                print("Good morning")
            elif 12 <= hour < 17:
#                 test_say("Good afternoon")
                print("Good afternoon")
            elif 17 <= hour < 20:
#                 test_say("Good evening")
                print("Good evening")
            else:
#                 test_say("Good night")
                print("Good night")

    dependencies = ["testaudio"]

    def initialize(self):
        print("Plugin One initialized.")

    def cleanup(self):
        print("Plugin One cleaned up.")