import requests


class Plugin:
    def __init__(self):
        pass

    def run(self, *args, **kwargs):
        text = kwargs["text"]
        target_language = kwargs["target_language"]
        return self.translate_text(text, target_language)

    @staticmethod
    def translate_text(text, target_language):
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={text}"
        response = requests.get(url)
        translation = response.json()[0][0][0]
        return translation
