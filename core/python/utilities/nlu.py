from groq import Groq
import json
import re
import os


# Load intents and patterns from JSON files
def load_intents():
    """Load intents from a JSON file and flatten the structure."""
    with open("../python/data/intent.json", 'r') as file:
        intents_data = json.load(file)

    # Flatten the intents into a list of examples with corresponding intent names
    intents_list = []
    for intent in intents_data['intents']:
        for example in intent['examples']:
            intents_list.append((example, intent['name']))  # Store tuple of (example, intent name)
    file.close()
    return intents_list


def load_patterns():
    """Load patterns from a JSON file."""
    # with open("../python/data/entity.json", 'r') as file:
    with open("../python/data/entity.json", 'r') as file:
        pattern_data = json.load(file)
    file.close()
    return pattern_data['entities']


# Preprocess the raw text data from user
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)  # Allow spaces
    return text.strip()


# Will match and extract the intent and entity from the user query
def match_query(text):
    intent = load_intents()
    pattern = load_patterns()
    with open("../python/data/.env", 'r') as f:
        api = f.read().replace("GROQ_API_KEY=",'')

    os.environ['GROQ_API_KEY'] = str(api)

    client = Groq(
        api_key=os.environ['GROQ_API_KEY'],
    )

    stream = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"use the below lists and get the intent and entity from the query/text given by the user. "
                           f"Only and only in form Intent: intent_name Entity: entity_name, give all the intent and "
                           f"entities that matches with the user given text and if it does not match any then just "
                           f"answer None. "
                           f"{intent}{pattern}"
            },
            {
                "role": "user",
                "content": f"{preprocess(text)}",
            }
        ],
        model="llama3-8b-8192",
        stream=False,
    )

    return str(stream.choices[0].message.content)


# # Main execution
# if __name__ == "__main__":
#     # Example query
#     query = "good morning, what is the weather? in india"
#     r = match_query(query)
#     # print(r)
#
#     # Find all intent-entity pairs
#     matches = re.findall(r"Intent:\s*(\w+)\s*Entity:\s*(\w+)", r)
#
#     # Extract and print results
#     res = {}
#     for intent, entity in matches:
#         # print(f"{intent} {entity}")
#         res[intent] = entity
#         print(res)
