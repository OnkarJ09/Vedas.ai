from gtts import gTTS
import os


class Plugin:
    @staticmethod
    def run(self, *args, **kwargs):
        text = kwargs.get("text", '')
        language = kwargs.get("language", '')
        if text and language:
            self.say(text, language)

    @staticmethod
    def say(text, language):
        """
        Convert text to speech and save it as an audio file.

        Parameters:
            text (str): The text to be spoken.
            language (str): The ISO 639-1 language code for the desired language.
        """

        tts = gTTS(text, lang=language, slow=False)
        tts.save("temp.mp3")
        os.system("mpg123 temp.mp3")
        os.remove("temp.mp3")
