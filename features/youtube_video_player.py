from features.audio import say
import pywhatkit


def yt_vdo_player(query):
    pywhatkit.playonyt(query)
    say(f"Playing {query} on YouTube")
    return f'{query}'
