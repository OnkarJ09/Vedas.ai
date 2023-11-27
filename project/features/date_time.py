from project.features.audio import say
import datetime


# It will return the current date and time in the format of "Sunday, 12 March 2023 10:00 AM"
def date_time():
    say(datetime.datetime.now().strftime("%A, %d %B, %Y %I:%M %p"))
    print(datetime.datetime.now().strftime("%A, %d %B, %Y %I:%M %p"))


# It will return the current date in the format of "Sunday, 12 March 2023"
def date():
    say(datetime.datetime.now().strftime("%A, %d %B ,%Y"))
    print(datetime.datetime.now().strftime("%A, %d %B ,%Y"))


# It will return the current time in the format of "10:00 AM"
def time():
    say(datetime.datetime.now().strftime("%I:%M %p"))
    print(datetime.datetime.now().strftime("%I:%M %p"))


# It will return the current day in the format of "Monday"
def day():
    say(datetime.datetime.now().strftime("%A"))
    print(datetime.datetime.now().strftime("%A"))


# It will return the current month in the format of "March"
def month():
    say(datetime.datetime.now().strftime("%B"))
    print(datetime.datetime.now().strftime("%B"))


# It will return the current year in the format of "2019"
def year():
    say(datetime.datetime.now().strftime("%Y"))
    print(datetime.datetime.now().strftime("%Y"))
