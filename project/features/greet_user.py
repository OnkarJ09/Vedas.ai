from project.features.audio import say
import datetime


def greetuser():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        say("Good morning")
        print("Good morning")
    elif hour >= 12 and hour < 17:
        say("Good afternoon")
        print("Good afternoon")
    elif hour >= 17 and hour < 20:
        say("Good evening")
        print("Good evening")
    else:
        say("Good night")
        print("Good night")
