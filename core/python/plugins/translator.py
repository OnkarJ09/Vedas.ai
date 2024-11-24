import requests


class Vedas:
    def __init__(self, **kwargs):
        self.keywords = ["translate", "translator"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    def matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def run(self, *args, **kwargs):
        if self.last_query:
            query_lower = self.last_query.lower()
            if "translate" in query_lower:
                text = query_lower.split("translate ")[1]
                target_language = query_lower.split("to ")[2]
                target_lan_code = Vedas.recognizer_lang_ids(target_language)
                return self.translate_text(text, str(target_lan_code))
            elif "translator" in query_lower:
                text = query_lower.split("translator ")[1]
                target_language = query_lower.split("to ")[2]
                target_lan_code = Vedas.recognizer_lang_ids(target_language)
                return self.translate_text(text, str(target_lan_code))


    @staticmethod
    def lang_id(language):
        languages = {
            "afrikaans": "af",
            "albanian": "sq",
            "amharic": "am",
            "arabic": "ar",
            "armenian": "hy",
            "assamese": "as",
            "aymara": "ay",
            "azerbaijani": "az",
            "bambara": "bm",
            "basque": "eu",
            "belarusian": "be",
            "bengali": "bn",
            "bhojpuri": "bho",
            "bosnian": "bs",
            "bulgarian": "bg",
            "catalan": "ca",
            "cebuano": "ceb",
            "chinese": "zh",
            "corsican": "co",
            "croatian": "hr",
            "czech": "cs",
            "danish": "da",
            "dhivehi": "dv",
            "dogri": "doi",
            "dutch": "nl",
            "english": "en",
            "esperanto": "eo",
            "estonian": "et",
            "ewe": "ee",
            "filipino (tagalog)": "fil",
            "finnish": "fi",
            "french": "fr",
            "frisian": "fy",
            "galician": "gl",
            "georgian": "ka",
            "german": "de",
            "greek": "el",
            "guarani": "gn",
            "gujarati": "gu",
            "haitian creole": "ht",
            "hausa": "ha",
            "hawaiian": "haw",
            "hebrew": "he",
            "hindi": "hi",
            "hmong": "hmn",
            "hungarian": "hu",
            "icelandic": "is",
            "igbo": "ig",
            "ilocano": "ilo",
            "indonesian": "id",
            "irish": "ga",
            "italian": "it",
            "japanese": "ja",
            "javanese": "jv",
            "kannada": "kn",
            "kazakh": "kk",
            "khmer": "km",
            "kinyarwanda": "rw",
            "konkani": "gom",
            "korean": "ko",
            "krio": "kri",
            "kurdish": "ku",
            "kurdish (sorani)": "ckb",
            "kyrgyz": "ky",
            "lao": "lo",
            "latin": "la",
            "latvian": "lv",
            "lingala": "ln",
            "lithuanian": "lt",
            "luganda": "lg",
            "luxembourgish": "lb",
            "macedonian": "mk",
            "maithili": "mai",
            "malagasy": "mg",
            "malay": "ms",
            "malayalam": "ml",
            "maltese": "mt",
            "maori": "mi",
            "marathi": "mr",
            "manipuri": "mni",
            "mizo": "lus",
            "mongolian": "mn",
            "myanmar (burmese)": "my",
            "nepali": "ne",
            "norwegian": "no",
            "nyanja": "ny",
            "odia": "or",
            "oromo": "om",
            "pashto": "ps",
            "persian": "fa",
            "polish": "pl",
            "portuguese (portugal, brazil)": "pt",
            "punjabi": "pa",
            "quechua": "qu",
            "romanian": "ro",
            "russian": "ru",
            "samoan": "sm",
            "sanskrit": "sa",
            "scots gaelic": "gd",
            "sepedi": "nso",
            "serbian": "sr",
            "sesotho": "st",
            "shona": "sn",
            "sindhi": "sd",
            "sinhala (sinhalese)": "si",
            "slovak": "sk",
            "slovenian": "sl",
            "somali": "so",
            "spanish": "es",
            "sundanese": "su",
            "swahili": "sw",
            "swedish": "sv",
            "tagalog (filipino)": "tl",
            "tajik": "tg",
            "tamil": "ta",
            "tatar": "tt",
            "telugu": "te",
            "thai": "th",
            "tigrinya": "ti",
            "tsonga": "ts",
            "turkish": "tr",
            "turkmen": "tk",
            "twi (akan)": "ak",
            "ukrainian": "uk",
            "urdu": "ur",
            "uyghur": "ug",
            "uzbek": "uz",
            "vietnamese": "vi",
            "welsh": "cy",
            "xhosa": "xh",
            "yiddish": "yi",
            "yoruba": "yo",
            "zulu": "zu"
        }

        language = language.lower()

        return languages.get(language, "Language not found")

    @staticmethod
    def recognizer_lang_ids(language):
        lang = language.lower()
        language_code = Vedas.lang_id(lang)
        return language_code

    @staticmethod
    def translate_text(text, target_language):
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={text}"
        response = requests.get(url)
        translation = response.json()[0][0][0]
        return translation

