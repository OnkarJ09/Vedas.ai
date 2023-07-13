from features import date_time, greet_user
from features.audio import say
import speech_recognition as sr


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

                #    Greetings
                if "good morning" in query:
                    greet_user.greetuser()

                elif "good afternoon" in query:
                    greet_user.greetuser()

                elif "good evening" in query:
                    greet_user.greetuser()

                elif "good night" in query:
                    greet_user.greetuser()

                #    Date & Time
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


Pragati.virtual_assistant()
