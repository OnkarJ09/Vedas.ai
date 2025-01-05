from groq import Groq
import json
import os
import re



# Load intents and patterns from JSON files
def load_intents():
    """Load intents from a JSON file and flatten the structure."""
    with open("../data/intent.json", 'r') as file:
        intents_data = json.load(file)

    # Flatten the intents into a list of examples with corresponding intent names
    intents_list = []
    for intent in intents_data['intents']:
        for example in intent['examples']:
            intents_list.append((example, intent['name']))  # Store tuple of (example, intent name)
    # print(intents_list)
    return intents_list

def load_patterns():
    """Load patterns from a JSON file."""
    with open("../data/entity.json", 'r') as file:
        pattern_data = json.load(file)
    # print(pattern_data)
    return pattern_data['entities']

# Preprocess the raw text data from user
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)  # Allow spaces
    # print(text.strip())
    return text.strip()

# Will match and extract the intent and entity from the user query
def match_query(text):
    intent = load_intents()
    pattern = load_patterns()
    with open("../data/.env") as f:
        read = f.read().replace("GROQ_API_KEY=", '')

    os.environ["GROQ_API_KEY"] = str(read)

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    stream = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"use the below lists and get the intent and entity from the query/text given by the user only in form Intent: intent_name Entity: entity_name give all the intent and entities that match and if it does not match any then just answer the user query in general as per yours knowledge{intent}{pattern}"
            },
            {
                "role": "user",
                "content": f"{text}",
            }
        ],
        model="llama3-8b-8192",
        stream=True,
    )

    for chunk in stream:
        print(chunk.choices[0].delta.content, end="")


# Main execution
if __name__ == "__main__":
    # Load intents and patterns
    # Example query
    query = "Good morning, what is the weather like today?"
    match_query(query)
