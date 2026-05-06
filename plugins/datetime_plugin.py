import datetime


class Vedas:
    def __init__(self, config=None, **kwargs):
        self.name = "datetime_plugin"
        self.description = "Provides current date, time, day, month, or year based on user query"
        self.parameters = ["input_data"]

        self.keywords = ["date", "time", "day", "month", "year"]

        self.dependencies = []
        self.tool_map = {}
        self.config = config or {}
        self.enabled = True
        self.last_query = None

    def matches_query(self, query):
        self.last_query = query.lower()
        return any(keyword in self.last_query for keyword in self.keywords)

    def run(self, input_data=None, state=None, **kwargs):
        print(f"[{self.name}] received:", input_data)

        # Determine query source (LLM args or keyword match)
        query = (self.last_query or input_data or "").lower()

        # Handle combined case first
        if "date" in query and "time" in query:
            return self.date_time()

        elif "date" in query:
            return self.date()

        elif "time" in query:
            return self.time()

        elif "day" in query:
            return self.day()

        elif "month" in query:
            return self.month()

        elif "year" in query:
            return self.year()

        # fallback
        return self.date_time()

    # Full date + time
    def date_time(self):
        return datetime.datetime.now().strftime("%A, %d %B %Y %I:%M %p")

    # Only date
    def date(self):
        return datetime.datetime.now().strftime("%A, %d %B %Y")

    # Only time
    def time(self):
        return datetime.datetime.now().strftime("%I:%M %p")

    # Day
    def day(self):
        return datetime.datetime.now().strftime("%A")

    # Month
    def month(self):
        return datetime.datetime.now().strftime("%B")

    # Year
    def year(self):
        return datetime.datetime.now().strftime("%Y")

    def __str__(self):
        return f"{self.name} ({self.keywords})"