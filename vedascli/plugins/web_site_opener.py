from .web_search import Vedas
from .audio import say
import webbrowser


class Vedas:
    def __init__(self, **kwargs):
        self.keywords = ["start"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    def matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def run(self, *args, **kwargs):
        if self.last_query:
            query_lower = self.last_query.lower()
            if "start" in query_lower:
                return self.web_site_open(query_lower)

    dependencies = ["web_search", "audio"]

    def web_site_open(self, query):
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
                if f"start {site[0]}" in query:
                    say(f"starting {site[0]}")
                    webbrowser.open(site[1])
                    if query:
                        handled = True
                        break
            if not handled:
                if query:
                    Vedas.search_and_open(self, query)

        except Exception as e:
            print(e)
            say("sorry, something went wrong. Try again")
