from .test_audio import test_say
import pywhatkit


class Test_Vedas:
    # Initial function for self declaration and some variables
    def test___init__(self, **kwargs):
        self.keywords = ["play on youtube", "play on yt", "play yt", "play youtube"]
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
            return self.test_yt_vdo_player(query_lower)

    # These are the dependencies that are required to run this function
    dependencies = ["test_audio"]

    def test_yt_vdo_player(self, query):
        query = query.replace("play on youtube", '')
        query = query.replace("play on yt", '')
        query = query.replace("play", '')
        query = query.replace("youtube", '')
        query = query.replace("yt", '')
        pywhatkit.playonyt(query)
        test_say(f"Playing {query}")
        print(f"Playing {query}")
