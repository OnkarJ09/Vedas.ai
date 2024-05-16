from vedascli.plugins.audio import Vedas
import datetime


class Vedas:
    def __init__(self):
        pass

    def match_query(self, query):
        q = {
            "date time": self.date_time,
            "day": self.day,
            "date": self.date,
            "time": self.time,
            "month": self.month,
            "year": self.year
        }
        for i in q[0]:
            if i in query:
                return i[1]

    def run(self, *args, **kwargs):
        query = self.match_query(kwargs["query"])
        return query

    dependencies = ["audio"]

    # It will return the current date and time in the format of "Sunday, 12 March 2023 10:00 AM"
    @staticmethod
    def date_time():
        print(f"now it's {datetime.datetime.now().strftime("%A, %d %B, %Y %I:%M %p")}")
        Vedas.say(f"now it's {datetime.datetime.now().strftime("%A, %d %B, %Y %I:%M %p")}")

    # It will return the current date in the format of "Sunday, 12 March 2023"
    @staticmethod
    def date():
        print(f"today is {datetime.datetime.now().strftime("%A, %d %B ,%Y")}")
        Vedas.say(f"today is {datetime.datetime.now().strftime("%A, %d %B ,%Y")}")

    # It will return the current time in the format of "10:00 AM"
    @staticmethod
    def time():
        print(f"it's {datetime.datetime.now().strftime("%I:%M %p")}")
        Vedas.say(f"it's {datetime.datetime.now().strftime("%I:%M %p")}")

    # It will return the current day in the format of "Monday"
    @staticmethod
    def day():
        print(f"it's {datetime.datetime.now().strftime("%A")}")
        Vedas.say(f"it's {datetime.datetime.now().strftime("%A")}")

    # It will return the current month in the format of "March"
    @staticmethod
    def month():
        print(f"it's {datetime.datetime.now().strftime("%B")}")
        Vedas.say(f"it's {datetime.datetime.now().strftime("%B")}")

    # It will return the current year in the format of "2019"
    @staticmethod
    def year():
        print(f"it's {datetime.datetime.now().strftime("%Y")}")
        Vedas.say(f"it's {datetime.datetime.now().strftime("%Y")}")
