import webbrowser


class Vedas:
    def __init__(self, config=None, **kwargs):
        self.name = "web_search_plugin"     # Name of the plugin

        # Description to help AI to better understand the purpose of the plugin and how to use it effectively.
        self.description = ("It searches the web for information based on user queries and "
                            "opens relevant web pages in the default browser.")
        self.parameters = ["input_data"]

        # Keywords to match from user query for execution
        self.keywords = [
            "search for", "find information on", "look up",
            "web search", "google", "bing", "duckduckgo"
        ]

        self.dependencies = []      # Dependencies for the plugin (e.g., external libraries, APIs)
        self.tool_map = {}
        self.config = config or {}
        self.enabled = True     # Flag to enable or disable the plugin
        self.last_query = None      # Store the last query for history and context, debugging and logging purpose

    def matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def run(self, input_data=None, **kwargs):
        return self.web_search(input_data)

    def web_search(self, query: str):
        # Get the query from the args or input_data or last_query (important for LLM + chaining)
        query = query.lower()

        if not query:
            return f"Could not understand request"

        # Replace the match keywords to get the actual user query
        for keyword in self.keywords:
            if keyword in query:
                query = query.replace(keyword, "").lower()

        # Open the search query in the default web browser using Google search
        webbrowser.open_new_tab("https://www.google.com/search?q=" + query)

        return f"Searching the web for: {query}"

    def __str__(self):
        return str(self.keywords)



if __name__ == "__main__":
    print(Vedas().run("search for the latest news on AI advancements"))