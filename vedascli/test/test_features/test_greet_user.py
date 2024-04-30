from vedascli.test.test_features.test_audio import test_say
import datetime
import pytest


@pytest.fixture(autouse=True)
def audio():
    return "Vedas.ai"


def test_greetuser():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        test_say("Good morning")
        print("Good morning")
    elif hour >= 12 and hour < 17:
        test_say("Good afternoon")
        print("Good afternoon")
    elif hour >= 17 and hour < 20:
        say("Good evening")
        print("Good evening")
    else:
        test_say("Good night")
        print("Good night")
