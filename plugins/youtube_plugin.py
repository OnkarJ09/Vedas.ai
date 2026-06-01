import webbrowser
import pywhatkit

class Ytvdoplayer(Exception):
    pass

class Vedas:
    def __init__(self, config=None, **kwargs):
        self.name = "youtube_plugin"  # Name of the plugin
        self.description = "It search and play videos on youtube"  # Description of the plugin
        self.parameters = ["input_data"]

        # Keywords to match from user query for execution
        self.keywords = [
            "youtube", "yt" , "y t"
        ]

        self.dependencies = []  # Dependencies for the plugin (e.g., external libraries, APIs)
        self.tool_map = {}
        self.config = config or {}
        self.enabled = True  # Flag to enable or disable the plugin
        self.last_query = None  # Store the last query for history and context, debugging and logging purpose
        self.key_matches = {
            "search for", "search on", "search", "play on", "play for", "play"
        }

    def matches_query(self, query):
        self.last_query = query
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.keywords)

    def run(self, input_data=None, **kwargs):
        query = input_data.lower()

        # Replace keyword 'yt'/'y t' with YouTube in query
        if "yt" in query or "y t" in query:
            query = query.replace("yt", "youtube")
            query = query.replace("y t", "youtube")

        """
            Check for the keywords,
            :keyword play & youtube - to play the video on youtube using pywhatkit
            :keyword search & youtube - to search the video on youtube using webbrowser
        """
        if "play" in query and "youtube" in query:
            try:    # Try to play video on YouTube
                return self.youtube_video_player(query)
            except Ytvdoplayer:     # Else search on YouTube for query
                return f"Could not play {query} on youtube, {self.youtube_video_player(query)}"

        elif "search" in query and "youtube" in query:
            return self.youtube_search(query)

         # Fallback (VERY IMPORTANT)
        return f"Sorry!! I couldn't understand your request. Please try again with a valid query"

    def youtube_search(self, search_term: str, **kwargs):
        """
            Searches on YouTube using request
        :param search_term: String
        :param kwargs:
        :return: open web browser and search results on YouTube
        """
        query = search_term.lower()


        # Replace the match keywords with empty string to get the actual user query
        query = self.replacement(query)

        # Try to process the request and open the search query in the default web browser using YouTube search
        try:
            url_link = f'https://www.youtube.com/results?search_query={query}'
            webbrowser.open(url_link)
            return f"Trying to search {query} on youtube..."
        except Ytvdoplayer:
            return "Sorry!! Please Try Again"

    def youtube_video_player(self, video_name: str, **kwargs):
        """
            Play a YouTube video on YouTube using pywhatkit
        :param video_name: string
        :param kwargs:
        :return: Open web browser and play the song
        """
        query = video_name.lower()

        ## Replace the match keywords with empty string to get the actual user query
        query = self.replacement(query)

        # Try to play the requested video on YouTube using pywhatkit
        try:
            pywhatkit.playonyt(query)
            return f"Trying to play {query} on youtube..."
        except Ytvdoplayer:
            return "Sorry!! Please Try Again"

    def replacement(self, query):
        """
                Replace the match keywords with empty string to get the actual user query
        :param query: string
        :return: string
        """
        for keyword in self.keywords:
            if keyword in query:
                query = query.replace(keyword, "")

        for key_match in self.key_matches:
            if key_match in query:
                query = query.replace(key_match, "")

        return query

    def __str__(self):
        return str(self.keywords)


if __name__ == "__main__":
    print(Vedas().run("search on youtube for the latest music videos"))
    # print(Vedas().run("play illahi on youtube"))
    # print(Vedas().youtube_search("search on youtube for the latest music videos"))
    # print(Vedas().youtube_video_player("play illahi on youtube"))