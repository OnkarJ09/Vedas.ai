import webbrowser
import pytest


@pytest.fixture
def querys():
    return "PRAGATI.ai"

def test_search_and_open(querys):
    search_url = f"https://www.google.com/search?q={querys}"
    webbrowser.open(search_url)
