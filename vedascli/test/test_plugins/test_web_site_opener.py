from .test_web_search import Test_Vedas
from .test_audio import test_say
import webbrowser


class Test_Vedas:
    def test___init__(self, **kwargs):
        self.keywords = ["start"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    def test_matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def test_run(self, *args, **kwargs):
        if self.last_query:
            query_lower = self.last_query.lower()
            if "start" in query_lower:
                return self.test_web_site_open(query_lower)

    dependencies = ["test_web_search", "test_audio"]

    def test_web_site_open(self, query):
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
                    test_say(f"starting {site[0]}")
                    webbrowser.open(site[1])
                    if query:
                        handled = True
                        break
            if not handled:
                if query:
                    Test_Vedas.test_search_and_open(self, query)

        except Exception as e:
            print(e)
            test_say("sorry, something went wrong. Try again")
