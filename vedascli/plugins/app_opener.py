from AppOpener import open, close, mklist, give_appnames
from .audio import say


class Vedas:
    def __init__(self, **kwargs):
        self.keywords = ["open", "close", "list"]
        self.dependencies = ["audio"]
        self.enabled = True
        self.last_query = None

    def match_query(self, query):
        self.last_query = query
        lower_query = query
        match = any(keyword in lower_query for keyword in self.keywords)
        print(f"Matching query: {lower_query} -> {match}")
        return match

    def run(self, *args, **kwargs):
        if self.last_query:
            query_lower = self.last_query.lower()
            if "open" in query_lower:
                return self.app_opener_open(query_lower)
            elif "close" in query_lower:
                return self.app_opener_close(query_lower)
            elif "list" in query_lower:
                return self.app_opener_list()

    dependencies = ["audio"]

    def app_opener_open(self, query):
        app_name = query.replace("open", '').strip()
        print(f"opening {app_name}")
        say(f"opening {app_name}")
        return open(app_name, match_closest=True)

    def app_opener_close(self, query):
        app_name = query.replace("close", '').strip()
        print(f"closing {app_name}")
        say(f"closing {app_name}")
        return close(app_name, match_closest=True, output=False)

    def app_opener_list(self):
        mklist(name='vedascli/data/app_data.json')
        print("Here is the list of apps")
        say("Here is the list of apps")
        return give_appnames()
