from AppOpener import open, close, mklist, give_appnames


def appopener_open(inp):
    app_name = inp.replace("open", '')
    open(app_name, match_closest=True)


def appopener_close(inp):
    app_name = inp.replace("close", '')
    close(app_name, match_closest=True, output=False)


def appopener_list(inp):
    mklist(name='app_data.json')
    give_appnames()
