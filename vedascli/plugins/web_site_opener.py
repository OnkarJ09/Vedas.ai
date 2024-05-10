from .web_search import search_and_open
from .audio import say
import webbrowser


def web_site_open(query):
    try:
        sites = [["youtube", 'https://www.youtube.com'],
                 ["facebook", 'https://www.facebook.com'],
                 ["instagram", 'https://www.instagram.com'],
                 ["w3schools", 'https://www.w3schools.com'],
                 ["w3schools learning", 'https://my-learning.w3schools.com'],
                 ["whatsapp", 'https://web.whatsapp.com'],
                 ["telegram", 'https://web.telegram.com'],
                 ["github", 'https://github.com'],
                 ["replit", 'https://replit.com'],
                 ["g mail", 'https://mail.google.com'],
                 ["google", 'https://www.google.com'],
                 ["google calendar", 'https://calendar.google.com'],
                 ["online python packages", 'https://pypi.org'],
                 ["chat g p t", 'https://chat.openai.com']]

        # if query == site[0]:
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"opening {site[0]}")
                webbrowser.open(site[1])
            # else:
            #     search_and_open(query)

    except Exception as e:
        print(e)
        say("sorry, something went wrong. Try again")
