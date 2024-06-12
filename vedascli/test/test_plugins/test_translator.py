from vedascli.utilities.lang_ids_for_recognizer import Vedas
import requests


class Test_Vedas:
    def test___init__(self, **kwargs):
        self.keywords = ["translate", "translator"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    def test_matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def test_run(self, *args, **kwargs):
        if self.last_query:
            query_lower = self.last_query.lower()
            if "translate" in query_lower:
                text = query_lower.split("translate ")[1]
                target_language = query_lower.split("to ")[2]
                target_lan_code = Vedas.recognizer_lang_ids(target_language)
                return self.test_translate_text(text, str(target_lan_code))
            elif "translator" in query_lower:
                text = query_lower.split("translator ")[1]
                target_language = query_lower.split("to ")[2]
                target_lan_code = Vedas.recognizer_lang_ids(target_language)
                return self.test_translate_text(text, str(target_lan_code))

    @staticmethod
    def test_translate_text(text, target_language):
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={text}"
        response = requests.get(url)
        translation = response.json()[0][0][0]
        return translation
