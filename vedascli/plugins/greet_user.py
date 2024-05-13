from vedascli.plugins.audio import say
import datetime
from vedascli.temp import PluginManager


class Plugin(PluginManager):
    def matches_query(self, query):
        return "good" in query.lower()

    @staticmethod
    def run(self):
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            # say("Good morning")
            print("Good morning")
        elif hour >= 12 and hour < 17:
            # say("Good afternoon")
            print("Good afternoon")
        elif hour >= 17 and hour < 20:
            # say("Good evening")
            print("Good evening")
        else:
            # say("Good night")
            print("Good night")

    dependencies = [datetime]

    # @staticmethod
    # def greet_user():
    #     hour = int(datetime.datetime.now().hour)
    #     if hour >= 0 and hour < 12:
    #         say("Good morning")
    #         print("Good morning")
    #     elif hour >= 12 and hour < 17:
    #         say("Good afternoon")
    #         print("Good afternoon")
    #     elif hour >= 17 and hour < 20:
    #         say("Good evening")
    #         print("Good evening")
    #     else:
    #         say("Good night")
    #         print("Good night")
