import webbrowser


class Ytvdoplayer(Exception):
    pass


class Vedas:
    # Initial function for self declaration and some variables
    def __init__(self, **kwargs):
        self.keywords = ["search on youtube", "search on youtube for", "search on yt", "search on yt for"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    # This function will match and check the query keywords if present
    def matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    # This will run the script if the query is matched
    def run(self, *args, **kwargs):
        if self.last_query:
            query_lower = str(self.last_query).lower()
            return self.youtube_video_search(query_lower)


    def youtube_video_search(self, query):
        query = query.replace("search on", '')
        query = query.replace("youtube for", '')
        query = query.replace("youtube", '')
        query = query.replace("yt for", '')
        query = query.replace("yt", '')
        query = query.replace("search on youtube for", '')
        try:
            url_link = f'https://www.youtube.com/results?search_query={query}'
            webbrowser.open(url_link)
            return f"Trying to search {query} on youtube..."
        except Ytvdoplayer:
            print("Sorry!! Please Try Again")
            return "Sorry!! Please Try Again"
