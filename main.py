from features import date_time, greet_user, websearch, weather
from features.appopener import appopener_open, appopener_close, appopener_list
from features.audio import say
import speech_recognition as sr
import webbrowser


# This will take user input from microphone as source
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query


class Pragati:
    def virtual_assistant():
        greet_user.greetuser()
        print("I am Pragati ai your personal virtual assistant")
        say("I am Pragati ai your personal virtual assistant")
        print("How can I help you?")
        say("How can I help you?")

        if __name__ == "__main__":
            while True:
                query = take_command().lower()

                ########################    Greet-User     #######################
                if "good morning" in query:
                    greet_user.greetuser()

                elif "good afternoon" in query:
                    greet_user.greetuser()

                elif "good evening" in query:
                    greet_user.greetuser()

                elif "good night" in query:
                    greet_user.greetuser()

                ########################    Date, Time, day, month, year   #######################
                elif "date" in query:

                    date_time.date()

                elif "time" in query:

                    date_time.time()

                elif "date and time" in query:
                    date_time.date_time()

                elif "day" in query:
                    date_time.day()

                elif "month" in query:
                    date_time.month()

                elif "year" in query:
                    date_time.year()

                ######################     Search Engine     #######################
                elif "search for" in query:
                    querys = query.replace("search for", '')
                    websearch.search_and_open(querys)
                    search_url = f"https://www.google.com/search?={querys}"
                    webbrowser.open(search_url)
                    say(f"ok, searching for {querys}")

                #####################      Weather     #############################
                elif "weather" in query:
                    b = query.replace("what is the weather in", '')
                    q = weather.get_weather_data(b)
                    say(q)
                    print(q)

                #####################      Open/Close Different apps     #############################
                elif "open" in query:
                    inp = query
                    appopener_open(inp)

                elif "close" in query:
                    inp = query
                    appopener_close(inp)

                elif "list of apps" in query:
                    appopener_list(inp)


Pragati.virtual_assistant()
