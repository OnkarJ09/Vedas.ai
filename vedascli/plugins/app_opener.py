from AppOpener import open, close, mklist, give_appnames


def app_opener_open(inp):
    app_name = inp.replace("open", '')
    open(app_name, match_closest=True)


def app_opener_close(inp):
    app_name = inp.replace("close", '')
    close(app_name, match_closest=True, output=False)


def app_opener_list():
    mklist(name='vedascli/data/app_data.json')
    give_appnames()
