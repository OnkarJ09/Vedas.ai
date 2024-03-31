from project.features import date_time, greet_user, weather, openai, wikipedia, youtube_video_player
from project.features import websearch, ai_chat
from project.features.appopener import appopener_open, appopener_close, appopener_list
from project.features.audio import say
import speech_recognition as sr
import webbrowser
import pyautogui


class Ytvdoplayer(Exception):
    pass


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
        return query
    except Exception as e:
        print(e)
        print("Say that again please...")
        # return 'None'
    return 'None'


class Vedas:
    @staticmethod
    def virtual_assistant():
        greet_user.greetuser()
        print("I am Vedas ai your personal virtual assistant")
        say("I am Vedas ai your personal virtual assistant")
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
                    appopener_list()

                ####################       Wikipedia    #########################
                elif "wikipedia" in query:
                    query = query.replace("search wikipedia", '')
                    wikipedia.wiki(query)

                ################    Opening Youtube_search   ####################
                elif "search on youtube for" in query:
                    query = query.replace("search on youtube for", '')
                    try:
                        say(f"Trying to search {query} on youtube")
                        webbrowser.open(url=f'https://www.youtube.com/results?search_query={query}')
                    except Ytvdoplayer:
                        say("Sorry!! Please Try Again")
                        print("Sorry!! Please Try Again")

                ################    Youtube Video Player    ###############
                elif "play" and "on youtube" in query:
                    query = query.replace("play", '')
                    youtube_video_player.yt_vdo_player(query)

                ################    Opening Different Web-sites    ##################
                elif "start" in query:
                    sites = [["youtube", 'https://www.youtube.com'],
                             ["facebook", 'https://www.facebook.com'],
                             ["instagram", 'https://www.instagram.com'],
                             ["w3schools", 'https://www.w3schools.com'],
                             ["w3schools learning", 'https://my-learning.w3schools.com'],
                             ["whatsapp", 'https://web.whatsapp.com'],
                             ["telegram", 'https://web.telegram.com'],
                             ["github", 'https://github.com'],
                             ["replit", 'https://replit.com'],
                             ["g mail", 'https://mail.google.com'],
                             ["google", 'https://www.google.com'],
                             ["google calendar", 'https://calendar.google.com'],
                             ["online python packages", 'https://pypi.org'],
                             ["chat g p t", 'https://chat.openai.com']]
                    for site in sites:
                        if f"open {site[0]}" in query:
                            say(f"opening {site[0]}")
                            webbrowser.open(site[1])

                ################    Windows Automation    ##################
                elif "maximize this window" in query:
                    pyautogui.hotkey('win', 'up')

                elif "minimize this window" in query:
                    pyautogui.hotkey('win', 'down')

                elif "shift this window" in query:
                    # this will shift windows on the top
                    if "shift this window to right" in query:
                        pyautogui.hotkey('win', 'right')

                    elif "shift this window to left" in query:
                        pyautogui.hotkey('win', 'left')

                    elif "shift this window to top right" in query:
                        with pyautogui.hold('win'):
                            pyautogui.press(['right', 'up'])

                    elif "shift this window to top left" in query:
                        with pyautogui.hold('win'):
                            pyautogui.press(['left', 'up'])

                    elif "shift this window to bottom right" in query:
                        with pyautogui.hold('win'):
                            pyautogui.press(['right', 'down'])

                    elif "shift this window to bottom left" in query:
                        with pyautogui.hold('win'):
                            pyautogui.press(['left', 'down'])

                ################    A.I.    ##################
                elif "using artificial intelligence" in query:
                    openai.ai(prompt=query)

                ################    Chatting with A.I   ##################
                else:
                    print("Chatting...")
                    ai_chat.chat(query)


Vedas.virtual_assistant()
