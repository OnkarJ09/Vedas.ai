from project.test.test_features import test_date_time, test_greet_user, test_weather, test_openai, test_wikipedia, test_youtube_video_player
from project.test.test_features import test_websearch, test_ai_chat
from project.test.test_features.test_appopener import test_appopener_open, test_appopener_close, test_appopener_list
from project.test.test_features.test_audio import test_say
import speech_recognition as sr
import webbrowser
import pyautogui
import pytest


@pytest.fixture(autouse=True)
def inp():
    return "Vedas.ai"


@pytest.fixture(autouse=True)
def audio():
    return "Vedas.ai"


class TestYtvdoplayer(Exception):
    pass


def test_take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query


class TestVedas:
    def test_virtual_assistant():
        test_greet_user.test_greetuser()
        print("I am Vedas ai your personal virtual assistant")
        test_say("I am Vedas ai your personal virtual assistant")
        print("How can I help you?")
        test_say("How can I help you?")

        if __name__ == "__main__":
            while True:
                query = test_take_command().lower()

                ########################    Greet-User     #######################
                if "good morning" in query:
                    test_greet_user.test_greetuser()
                    assert 'good' in query

                elif "good afternoon" in query:
                    greet_user.greetuser()
                    assert 'good' in query

                elif "good evening" in query:
                    test_greet_user.test_greetuser()
                    assert 'good' in query

                elif "good night" in query:
                    test_greet_user.test_greetuser()
                    assert 'good' in query

                ########################    Date, Time, day, month, year   #######################
                elif "date" in query:
                    test_date_time.test_date()
                    assert 'date' in query

                elif "time" in query:
                    test_date_time.test_time()
                    assert 'time' in query

                elif "date and time" in query:
                    test_date_time.test_date_time()
                    assert 'date' or 'time' in query

                elif "day" in query:
                    test_date_time.test_day()
                    assert 'day' in query

                elif "month" in query:
                    test_date_time.test_month()
                    assert 'month' in query

                elif "year" in query:
                    test_date_time.test_year()
                    assert 'year' in query

                ######################     Search Engine     #######################
                elif "search for" in query:
                    querys = query.replace("search for", '')
                    test_websearch.test_search_and_open(querys)
                    search_url = f"https://www.google.com/search?={querys}"
                    webbrowser.open(search_url)
                    test_say(f"ok, searching for {querys}")
                    assert 'search' in query

                #####################      Weather     #############################
                elif "weather" in query:
                    b = query.replace("what is the weather in", '')
                    q = test_weather.test_get_weather_data(b)
                    test_say(q)
                    print(q)
                    assert 'weather' in query

                #####################      Open/Close Different apps     #############################
                elif "open" in query:
                    inp = query
                    test_appopener_open(inp)
                    assert 'open' in query

                elif "close" in query:
                    inp = query
                    test_appopener_close(inp)
                    assert 'close' in query

                elif "list of apps" in query:
                    test_appopener_list()
                    assert 'list' in query

                ####################       Wikipedia    #########################
                elif "wikipedia" in query:
                    query = query.replace("search wikipedia", '')
                    test_wikipedia.test_wiki(query)
                    assert 'wikipedia' in query

                ################    Opening Youtube_search   ####################
                elif "search on youtube for" in query:
                    query = query.replace("search on youtube for", '')
                    try:
                        test_say(f"Trying to search {query} on youtube")
                        webbrowser.open(url=f'https://www.youtube.com/results?search_query={query}')
                    except TestYtvdoplayer:
                        test_say("Sorry!! Please Try Again")
                        print("Sorry!! Please Try Again")
                        assert 'youtube' in query

                ################    Youtube Video Player    ###############
                elif "play" and "on youtube" in query:
                    query = query.replace("play", '')
                    test_youtube_video_player.test_yt_vdo_player(query)
                    assert 'play' or 'youtube' in query

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
                    assert f'{sites[0]}' in query

                ################    Windows Automation    ##################
                elif "maximize this window" in query:
                    pyautogui.hotkey('win', 'up')
                    assert 'window' in query

                elif "minimize this window" in query:
                    pyautogui.hotkey('win', 'down')
                    assert 'window' in query

                elif "shift this window" in query:
                    # this will shift windows on the top
                    if "shift this window to right" in query:
                        pyautogui.hotkey('win', 'right')
                        assert 'window' in query

                    elif "shift this window to left" in query:
                        pyautogui.hotkey('win', 'left')
                        assert 'window' in query

                    elif "shift this window to top right" in query:
                        with pyautogui.hold('win'):
                            pyautogui.press(['right', 'up'])
                        assert 'window' in query

                    elif "shift this window to top left" in query:
                        with pyautogui.hold('win'):
                            pyautogui.press(['left', 'up'])
                        assert 'window' in query

                    elif "shift this window to bottom right" in query:
                        with pyautogui.hold('win'):
                            pyautogui.press(['right', 'down'])
                        assert 'window' in query

                    elif "shift this window to bottom left" in query:
                        with pyautogui.hold('win'):
                            pyautogui.press(['left', 'down'])
                        assert 'window' in query

                ################    A.I.    ##################
                elif "using artificial intelligence" in query:
                    test_openai.test_ai(prompt=query)
                    assert 'artificial' in query

                ################    Chatting with A.I   ##################
                else:
                    print("Chatting...")
                    test_ai_chat.test_chat(query)
                    assert 'Vedas.ai' in query


TestVedas.test_virtual_assistant()
