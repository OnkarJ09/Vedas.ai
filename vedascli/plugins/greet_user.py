from vedascli.plugins.audio import Plugin
import datetime


class Plugin:
    def matches_query(self, query):
        querys = {
            "morning",
            "afternoon",
            "evening",
            "night",
        }
        for q in querys:
            if q in query:
                return q.lower()

    @staticmethod
    def run(self):
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            Plugin.say("Good morning")
            print("Good morning")
        elif 12 <= hour < 17:
            Plugin.say("Good afternoon")
            print("Good afternoon")
        elif 17 <= hour < 20:
            Plugin.say("Good evening")
            print("Good evening")
        else:
            Plugin.say("Good night")
            print("Good night")

    dependencies = ["audio"]
