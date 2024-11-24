import wikipedia


class Vedas:
    def __init__(self, **kwargs):
        self.keywords = ["wikipedia", "wiki"]
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
            if "wikipedia" in query_lower:
                return self.wiki(query_lower)


    def wiki(self, query):
        """
        Searches wikipedia for the given query and returns the first result.
        """
        query = query.replace("wikipedia", '')
        query = query.replace("wiki", '')
        query = query.replace("search", '')
        query = query.replace("for", '')
        # results = wikipedia.search(query)
        if query:
            return wikipedia.summary(str(query), sentences=2)
        else:
            return "No results found."
