import re

def normalize_text(text):
    text = text.lower().strip()

    # collapse repeated characters
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    # remove excessive repeated words
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text)

    # fix common stretched words manually
    replacements = {
        "helo": "hello",
        "helllo": "hello",
        "heyy": "hey",
        "hii": "hi"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text