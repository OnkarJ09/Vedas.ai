from AppOpener import open, close, mklist, give_appnames
from vedascli.plugins.audio import Vedas


class Vedas:
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

    @staticmethod
    def app_opener_open(query):
        app_name = query.replace("open", '')
        Vedas.say(f"opening {app_name}")
        open(app_name, match_closest=True)

    @staticmethod
    def app_opener_close(query):
        app_name = query.replace("close", '')
        Vedas.say(f"closing {app_name}")
        close(app_name, match_closest=True, output=False)

    @staticmethod
    def app_opener_list():
        mklist(name='vedascli/data/app_data.json')
        Vedas.say("Here is the list of apps")
        give_appnames()
