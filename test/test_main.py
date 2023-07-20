from test.test_features import test_, test_greet_user, test_websearch, test_weather, test_openai, test_ai_chat, \
    test_wikipedia
from test.test_features.test_appopener import test_appopener_open, test_appopener_close, test_appopener_list
from test.test_features.test_audio import test_say
import speech_recognition as sr
import webbrowser
import pyautogui
import pytest

@pytest.fixture(autouse=True)
def query():
    return "PRAGATI.ai"

@pytest.fixture(autouse=True)
def inp():
    return "PRAGATI.ai"

@pytest.fixture(autouse=True)
def audio():
    return "PRAGATI.ai"

def test_take_command():
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


class TestPragati:
    def test_virtual_assistant():
        test_greet_user.test_greetuser()
        print("I am Pragati ai your personal virtual assistant")
        test_say("I am Pragati ai your personal virtual assistant")
        print("How can I help you?")
        test_say("How can I help you?")

        if __name__ == "__main__":
            while True:
                query = test_take_command().lower()

                ########################    Greet-User     #######################
                if "good morning" in query:
                    test_greet_user.test_greetuser()

                elif "good afternoon" in query:
                    test_greet_user.test_greetuser()

                elif "good evening" in query:
                    test_greet_user.test_greetuser()

                elif "good night" in query:
                    test_greet_user.test_greetuser()

                ########################    Date, Time, day, month, year   #######################
                elif "date" in query:
                    test_date_time.test_date()

                elif "time" in query:
                    test_date_time.test_time()

                elif "date and time" in query:
                    test_date_time.test_date_time()

                elif "day" in query:
                    test_date_time.test_day()

                elif "month" in query:
                    test_date_time.test_month()

                elif "year" in query:
                    test_date_time.test_year()

                ######################     Search Engine     #######################
                elif "search for" in query:
                    querys = query.replace("search for", '')
                    test_websearch.test_search_and_open(querys)
                    search_url = f"https://www.google.com/search?={querys}"
                    webbrowser.open(search_url)
                    test_say(f"ok, searching for {querys}")

                #####################      Weather     #############################
                elif "weather" in query:
                    b = query.replace("what is the weather in", '')
                    q = test_weather.test_get_weather_data(b)
                    test_say(q)
                    print(q)

                #####################      Open/Close Different apps     #############################
                elif "open" in query:
                    inp = query
                    test_appopener_open(inp)

                elif "close" in query:
                    inp = query
                    test_appopener_close(inp)

                elif "list of apps" in query:
                    test_appopener_list()

                ####################       Wikipedia    #########################
                elif "wikipedia" in query:
                    query = query.replace("search wikipedia", '')
                    test_wikipedia.test_wiki(query)

                ################    Opening Youtube_search   ####################
                elif "youtube" in query:
                    test_say("what you want to search")
                    print("what you want to search?")
                    q = test_take_command().lower()
                    q = q.replace("search for", "")
                    webbrowser.open(f"https://www.youtube.com/results?search_query={q}")
                    test_say(f"searching on youtube for {q}")

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
                            test_say(f"opening {site[0]}")
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
                    test_openai.test_ai(prompt=query)

                ################    Chatting with A.I   ##################
                else:
                    print("Chatting...")
                    test_ai_chat.test_chat(query)


TestPragati.test_virtual_assistant()
