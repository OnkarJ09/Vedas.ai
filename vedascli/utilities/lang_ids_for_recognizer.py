from vedascli.data.lang_ids import lang_id

class Plugin:
    @staticmethod
    def run(self, *args, **kwargs):
        language = kwargs.get("language", '')
        if language:
            language_code = self.recognizer_lang_ids(self, language)
            return language_code

    @staticmethod
    def recognizer_lang_ids(language):
        lang = language.lower()
        language_code = lang_id(lang)
        return language_code
