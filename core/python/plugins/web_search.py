import webbrowser


class Vedas:
    def __init__(self, **kwargs):
        self.keywords = ["search for"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    def matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def run(self, *args, **kwargs):
        if self.last_query:
            query = self.last_query.lower()
            return self.search_and_open(query)

    def search_and_open(self, query):
        query = query.replace("search", '')
        query = query.replace("for", '')
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        return "Opening " + query

