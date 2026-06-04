from manager.env_manager import DEFAULT_LANGUAGE_CODE
import wikipedia

class Vedas:
    def __init__(self, config=None, **kwargs):
        self.name = "wikipedia_plugin"  # Name of the plugin
        self.description = "This plugin helps with Wikipedia searches and information retrieval."  # Description of the plugin
        self.parameters = ["input_data"]

        # Keywords to match from user query for execution
        self.keywords = [
            "wikipedia", "wiki"
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
        query = input_data.lower()
        if query:
            return self.wikipedia(query, result_lang=DEFAULT_LANGUAGE_CODE)
        else:
            return "No query recognized"

    def wikipedia(self, search_term, **kwargs):
        """
            This plugin helps with Wikipedia searches and information retrieval.
        :param search_term: str -> search term
        :param kwargs:
        :return: str -> search result
        """
        result_lang = kwargs.get("result_lang", "en")
        # Set the language for Wikipedia searches based on the result_lang parameter
        wikipedia.set_lang(result_lang)

        # Replace the match keywords to get the actual user query
        search_term = search_term.replace("wikipedia", '')
        search_term = search_term.replace("wiki", '')
        search_term = search_term.replace("search", '')
        search_term = search_term.replace("for", '')
        search_term = search_term.replace("on", '')

        # Try to search and retrieve information
        try:
            if search_term:     # Search only if there is a search term (query) found
                return wikipedia.summary(str(search_term), sentences=2)
            else:           # If no search term is found, return a message indicating that no results were found
                return "No results found"

        # For handling different types of exceptions
        except wikipedia.exceptions.PageError:
            return "No results found"
        except wikipedia.exceptions.DisambiguationError:
            return "No results found"
        except wikipedia.exceptions.WikipediaException:
            return "No results found"
        except Exception as e:
            return "An error occurred"


    def __str__(self):
        return str(self.keywords)


if __name__ == "__main__":
    print(Vedas().run("search wikipedia for artificial intelligence"))
