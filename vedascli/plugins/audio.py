from gtts import gTTS
import os


def say(text, language):
    """
    Convert text to speech and save it as an audio file.

    Parameters:
        text (str): The text to be spoken.
        language (str): The ISO 639-1 language code for the desired language.
    """
    # Create gTTS object with the specified language
    tts = gTTS(text, lang=language, slow=False)

    # Save the speech as a temporary audio file
    tts.save("temp.mp3")

    # Play the audio file
    os.system("mpg123 temp.mp3")  # You can use any audio player you prefer

    # Delete the temporary audio file
    os.remove("temp.mp3")
