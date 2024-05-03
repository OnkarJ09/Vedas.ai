from vedascli.data.lang_ids import lang_id


def recognizer_lang_ids():
    lang = input("Enter a language to communicate for this session: ").lower()
    language_code = lang_id(lang)
    return language_code
