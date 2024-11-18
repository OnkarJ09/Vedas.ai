class Vedas:
    def __init__(self):
        self.keywords = ["hello", "greet"]

    def matches_query(self, query):
        return any(keyword in query.lower() for keyword in self.keywords)

    def run(self, *args, **kwargs):
        print("Hello! How can I assist you today?")
        return "Hello! How can I assist you today?"

    def initialize(self):
        print("Plugin One initialized.")

    def cleanup(self):
        print("Plugin One cleaned up.")