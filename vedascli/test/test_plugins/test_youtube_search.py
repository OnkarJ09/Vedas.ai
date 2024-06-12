from .test_audio import test_say
import webbrowser


class Test_Ytvdoplayer(Exception):
    pass


class Test_Vedas:
    # Initial function for self declaration and some variables
    def test___init__(self, **kwargs):
        self.keywords = ["search on youtube", "search on youtube for", "search on yt", "search on yt for"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    # This function will match and check the query keywords if present
    def test_matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    # This will run the script if the query is matched
    def test_run(self, *args, **kwargs):
        if self.last_query:
            query_lower = str(self.last_query).lower()
            return self.test_youtube_video_search(query_lower)

    # These are the dependencies that are required to run this function
    dependencies = ["test_audio"]

    def test_youtube_video_search(self, query):
        query = query.replace("search on", '')
        query = query.replace("youtube for", '')
        query = query.replace("youtube", '')
        query = query.replace("yt for", '')
        query = query.replace("yt", '')
        query = query.replace("search on youtube for", '')
        try:
            url_link = f'https://www.youtube.com/results?search_query={query}'
            webbrowser.open(url_link)
            test_say(f"Trying to search {query} on youtube")
        except Test_Ytvdoplayer:
            print("Sorry!! Please Try Again")
            test_say("Sorry!! Please Try Again")
