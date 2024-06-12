from .test_audio import test_say
import datetime


class Test_Vedas:
    def test___init__(self, **kwargs):
        self.keywords = ["date time", "day", "date", "time", "month", "year"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    def test_matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def test_run(self, *args, **kwargs):
        if self.last_query:
            query_lower = self.last_query.lower()
            if "date time" in query_lower:
                return self.test_date_time()
            elif "date" in query_lower:
                return self.test_date()
            elif "time" in query_lower:
                return self.test_time()
            elif "day" in query_lower:
                return self.test_day()
            elif "month" in query_lower:
                return self.test_month()
            elif "year" in query_lower:
                return self.test_year()

    dependencies = ["test_audio"]

    # It will return the current date and time in the format of "Sunday, 12 March 2023 10:00 AM"
    def test_date_time(self):
        q = datetime.datetime.now().strftime("%A, %d %B, %Y %I:%M %p")
        print(q)
        test_say(q)
        return q
        # say(f"now it's {datetime.datetime.now().strftime("%A, %d %B, %Y %I:%M %p")}")

    # It will return the current date in the format of "Sunday, 12 March 2023"
    def test_date(self):
        q = datetime.datetime.now().strftime("%A, %d %B, %Y")
        print(q)
        test_say(q)
        return q
        # say(f"today is {datetime.datetime.now().strftime("%A, %d %B ,%Y")}")

    # It will return the current time in the format of "10:00 AM"
    def test_time(self):
        q = datetime.datetime.now().strftime("%I:%M %p")
        print(q)
        test_say(q)
        return q

    # It will return the current day in the format of "Monday"
    def test_day(self):
        q = datetime.datetime.now().strftime("%A")
        print(q)
        test_say(q)
        return q

    # It will return the current month in the format of "March"
    def test_month(self):
        q = datetime.datetime.now().strftime("%B")
        print(q)
        test_say(q)
        return q

    # It will return the current year in the format of "2019"
    def test_year(self):
        q = datetime.datetime.now().strftime("%Y")
        print(q)
        test_say(q)
        return q
