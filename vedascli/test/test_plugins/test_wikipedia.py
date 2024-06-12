from .test_audio import test_say
import wikipedia


class Test_Vedas:
    def test___init__(self, **kwargs):
        self.keywords = ["wikipedia", "wiki"]
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
            if "wikipedia" in query_lower:
                return self.test_wiki(query_lower)

    dependencies = ["test_audio"]

    def test_wiki(self, query):
        """
        Searches wikipedia for the given query and returns the first result.
        """
        query = query.replace("wikipedia", '')
        query = query.replace("wiki", '')
        query = query.replace("search", '')
        query = query.replace("for", '')
        query = query.replace(" ", '')
        # results = wikipedia.search(query)
        if query:
            test_say(wikipedia.summary(str(query), sentences=2))
        else:
            return "No results found."
