import requests
import json


def translate(text, target_language):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={text}"
    response = requests.get(url=url)
    translated_text = response.json()[0][0][0]
    print("[DEBUG] Translation API Response:", response.json())
    print("[DEBUG] Translation API Response:", translated_text)

    # For debugging
    print(f"[DEBUG] Translated Text: {translated_text}")

    return translated_text


if __name__ == "__main__":
    translate("Hello", "es")
    translate("Hello", "hi")
