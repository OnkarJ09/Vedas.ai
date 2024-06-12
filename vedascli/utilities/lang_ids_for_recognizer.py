from vedascli.data.lang_ids import lang_id

class Vedas:
    def __init__(self):
        pass

    @staticmethod
    def recognizer_lang_ids(language):
        lang = language.lower()
        language_code = lang_id(lang)
        return language_code
