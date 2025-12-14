import datetime

def date_time(query):
    query = query.lower()

    if "date" in query and "time" in query:
        return datetime.datetime.strftime(datetime.datetime.now(),"%A %b %d %Y %I:%M %p")

    elif "date" in query:
        return datetime.datetime.strftime(datetime.datetime.now(),"%A %b %d %Y")

    elif "time" in query:
        return datetime.datetime.strftime(datetime.datetime.now(),"%H:%M:%S")

    elif "day" in query:
        return datetime.datetime.strftime(datetime.datetime.now(),"%d")

    elif "month" in query:
        return datetime.datetime.strftime(datetime.datetime.now(),"%B")

    elif "year" in query:
        return datetime.datetime.strftime(datetime.datetime.now(),"%Y")

    else:
        return None


if __name__ == "__main__":
    print(date_time("date"))
    print(date_time("time"))
    print(date_time("day"))
    print(date_time("month"))
    print(date_time("year"))
    print(date_time("date time"))
