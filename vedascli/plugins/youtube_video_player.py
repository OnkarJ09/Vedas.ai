from vedascli.plugins.audio import say
import pywhatkit


def yt_vdo_player(query):
    query = query.replace("play", '')
    pywhatkit.playonyt(query)
    say(f"Playing {query}")
    print(f"Playing {query}")
