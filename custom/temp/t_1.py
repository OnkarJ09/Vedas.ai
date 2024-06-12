import fasttext


def detect_lang(text):
    model = fasttext.load_model('lid.176.bin')
    lang = model.predict(text, k=1)[0]
    return lang[0].replace("__label__", "")


print(detect_lang("tariq"))
