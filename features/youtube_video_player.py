from features.audio import say
import pywhatkit


def yt_vdo_player(query):
    say(f"Playing {query} on YouTube")
    pywhatkit.playonyt(query)
