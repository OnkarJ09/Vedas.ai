from AppOpener import open, close, mklist, give_appnames
from vedascli.plugins.audio import Plugin


class Plugin:
    def match_query(self, query):
        querys = {
            "open": self.app_opener_open,
            "close": self.app_opener_close,
            "app list": self.app_opener_list
        }
        for q in querys[0]:
            if q in query:
                return q[1]

    # @staticmethod
    def run(self, *args, **kwargs):
        query = self.match_query(kwargs["query"])
        return query

    dependencies = ["vedascli/data/app_data.json", "audio"]

    def app_opener_open(self, query):
        app_name = query.replace("open", '')
        Plugin.say(f"opening {app_name}")
        open(app_name, match_closest=True)

    def app_opener_close(self, query):
        app_name = query.replace("close", '')
        Plugin.say(f"closing {app_name}")
        close(app_name, match_closest=True, output=False)

    def app_opener_list(self):
        mklist(name='vedascli/data/app_data.json')
        Plugin.say("Here is the list of apps")
        give_appnames()
