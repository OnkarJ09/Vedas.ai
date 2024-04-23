from gtts import gTTS
import playsound


def say(audio, lang='hi'):
    tts = gTTS(text=audio, lang=lang, slow=False)
    tts.save("output.mp3")
    playsound.playsound("output.mp3")
