import datetime


class Vedas:
    def __init__(self, config=None, **kwargs):
        self.name = "datetime_plugin"
        self.description = "Provides current date, time, day, month, or year based on user query"
        self.parameters = ["input_data"]

        # Intent phrases for date/time queries
        self.keywords = [
            "what time", "what's the time", "what is the time", "current time", "tell me the time", "time now", "time please",
            "what date", "what's the date", "what is the date", "today's date", "current date", "date today",
            "what day", "what's the day", "what is the day", "which day", "day is today", "day is it",
            "what month", "what's the month", "what is the month", "which month", "current month",
            "what year", "what's the year", "what is the year", "which year", "current year",
            "date and time", "time and date", "datetime"
        ]

        # Standalone 1-word queries when the user just asks for the time/date directly
        self.standalone_words = ["time", "date", "day", "month", "year", "today", "datetime"]

        self.dependencies = []
        self.tool_map = {}
        self.config = config or {}
        self.enabled = True
        self.last_query = None

    def matches_query(self, query):
        q = (query or "").strip().lower()
        self.last_query = q
        if q in self.standalone_words:
            return True
        return any(keyword in q for keyword in self.keywords)

    def run(self, input_data=None, state=None, **kwargs):
        print(f"[{self.name}] received:", input_data)

        query = (input_data or self.last_query or "").strip().lower()

        # Handle combined date + time
        if any(p in query for p in ["date and time", "time and date", "datetime"]) or query in ["date and time", "time and date"]:
            return self.date_time()

        # Year intent (avoid matching general words like "final year", "next year")
        if any(p in query for p in ["what year", "what's the year", "what is the year", "which year", "current year"]) or query == "year":
            return self.year()

        # Time intent
        if any(p in query for p in ["what time", "what's the time", "what is the time", "current time", "tell me the time", "time now", "time please"]) or query == "time":
            return self.time()

        # Date intent
        if any(p in query for p in ["what date", "what's the date", "what is the date", "today's date", "current date", "date today"]) or query in ["date", "today"]:
            return self.date()

        # Day intent
        if any(p in query for p in ["what day", "what's the day", "what is the day", "which day", "day is today", "day is it"]) or query == "day":
            return self.day()

        # Month intent
        if any(p in query for p in ["what month", "what's the month", "what is the month", "which month", "current month"]) or query == "month":
            return self.month()

        # Standalone date/time fallback if explicitly invoked
        if query in self.standalone_words:
            return self.date_time()

        # Return None for conversational context so execute_pipeline falls back to LLM chat
        return None

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