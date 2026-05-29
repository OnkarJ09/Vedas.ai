import webbrowser

class Ytvdoplayer(Exception):
    pass

class Vedas:
    def __init__(self, config=None, **kwargs):
        self.name = "youtube_plugin"  # Name of the plugin
        self.description = "It search and play videos on youtube"  # Description of the plugin
        self.parameters = ["input_data"]

        # Keywords to match from user query for execution
        self.keywords = [
            "youtube", "search on youtube", "search youtube for",
            "search on yt", "search on yt for", "yt", "youtube for"
        ]

        self.dependencies = []  # Dependencies for the plugin (e.g., external libraries, APIs)
        self.tool_map = {}
        self.config = config or {}
        self.enabled = True  # Flag to enable or disable the plugin
        self.last_query = None  # Store the last query for history and context, debugging and logging purpose

    def matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def run(self, input_data=None, **kwargs):
        query = (self.last_query or input_data or "").lower()

    def youtube_search(self, search_term: str, **kwargs):
        query = search_term.lower()

        # Replace the match keywords with empty string to get the actual user query
        for keyword in self.keywords:
            if keyword in query:
                query = query.replace(keyword, "")

        # Try to process the request and open the search query in the default web browser using YouTube search
        try:
            url_link = f'https://www.youtube.com/results?search_query={query}'
            webbrowser.open(url_link)
            return f"Trying to search {query} on youtube..."
        except Ytvdoplayer:
            print("Sorry!! Please Try Again")
            return "Sorry!! Please Try Again"

    def __str__(self):
        return str(self.keywords)
