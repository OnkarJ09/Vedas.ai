from .audio import say
import webbrowser


class Ytvdoplayer(Exception):
    pass


def youtube_video_search(query):
    query = query.replace("search on youtube for", '')
    try:
        say(f"Trying to search {query} on youtube")
        webbrowser.open(url=f'https://www.youtube.com/results?search_query={query}')
    except Ytvdoplayer:
        say("Sorry!! Please Try Again")
        print("Sorry!! Please Try Again")
