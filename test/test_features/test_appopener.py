from AppOpener import open, close, mklist, give_appnames
import pytest


@pytest.fixture(autouse=True)
def inp():
    return "PRAGATI.ai"

def test_appopener_open(inp):
    app_name = inp.replace("open", '')
    open(app_name, match_closest=True)


def test_appopener_close(inp):
    app_name = inp.replace("close", '')
    close(app_name, match_closest=True, output=False)


def test_appopener_list():
    mklist(name='app_data.json')
    give_appnames()
