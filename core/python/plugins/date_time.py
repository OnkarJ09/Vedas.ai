import datetime


class Vedas:
    def __init__(self, **kwargs):
        self.keywords = ["date time", "day", "date", "time", "month", "year"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    def matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def run(self, *args, **kwargs):
        if self.last_query:
            query_lower = self.last_query.lower()
            if "date time" in query_lower:
                return self.date_time()
            elif "date" in query_lower:
                return self.date()
            elif "time" in query_lower:
                return self.time()
            elif "day" in query_lower:
                return self.day()
            elif "month" in query_lower:
                return self.month()
            elif "year" in query_lower:
                return self.year()

    # dependencies = ["audio"]

    # It will return the current date and time in the format of "Sunday, 12 March 2023 10:00 AM"
    def date_time(self):
        q = datetime.datetime.now().strftime("%A, %d %B, %Y %I:%M %p")
        print(q)
        return q

    # It will return the current date in the format of "Sunday, 12 March 2023"
    def date(self):
        q = datetime.datetime.now().strftime("%A, %d %B, %Y")
        print(q)
        return q

    # It will return the current time in the format of "10:00 AM"
    def time(self):
        q = datetime.datetime.now().strftime("%I:%M %p")
        print(q)
        return q

    # It will return the current day in the format of "Monday"
    def day(self):
        q = datetime.datetime.now().strftime("%A")
        print(q)
        return q

    # It will return the current month in the format of "March"
    def month(self):
        q = datetime.datetime.now().strftime("%B")
        print(q)
        return q

    # It will return the current year in the format of "2019"
    def year(self):
        q = datetime.datetime.now().strftime("%Y")
        print(q)
        return q
