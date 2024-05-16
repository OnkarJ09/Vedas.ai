from vedascli.plugins.web_search import Plugin
from vedascli.plugins.audio import Plugin
import webbrowser


class Plugin:
    def __init__(self):
        pass

    def match_query(self, query):
        if "start" in query:
            return query.lower()

    def run(self, *args, **kwargs):
        query = self.match_query(kwargs["query"])
        if query:
            self.web_site_open(query)

    @staticmethod
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

            for site in sites:
                if f"open {site[0]}" in query:
                    Plugin.say(f"opening {site[0]}")
                    webbrowser.open(site[1])
                    if query:
                        handled = True
                        break
            if not handled:
                if query:
                    Plugin.search_and_open(query)

        except Exception as e:
            print(e)
            Plugin.say("sorry, something went wrong. Try again")
