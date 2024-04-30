from vedascli.plugins.audio import say
import pywhatkit


def yt_vdo_player(query):
    pywhatkit.playonyt(query)
    say(f"Playing {query}")
    # return f'{query}'
