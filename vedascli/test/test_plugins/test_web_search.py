from .test_audio import test_say
import webbrowser


class Test_Vedas:
    def test___init__(self, **kwargs):
        self.keywords = ["search for"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    def test_matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def test_run(self, *args, **kwargs):
        if self.last_query:
            query = self.last_query.lower()
            return self.test_search_and_open(query)

    dependencies = ["test_audio"]

    def test_search_and_open(self, query):
        query = query.replace("search", '')
        query = query.replace("for", '')
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        test_say(f"ok, searching for {query}")
