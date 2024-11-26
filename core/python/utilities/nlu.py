import json
import re
from rapidfuzz import process

# Load intents and patterns from JSON files
def load_intents(file_path):
    """Load intents from a JSON file and flatten the structure."""
    with open(file_path, 'r') as file:
        intents_data = json.load(file)

    # Flatten the intents into a list of examples
    intents_list = []
    for intent in intents_data['intents']:
        intents_list.extend(intent['examples'])  # Add all examples to the list
    return intents_list

def load_patterns(file_path):
    """Load patterns from a JSON file."""
    with open(file_path, 'r') as file:
        pattern_data = json.load(file)
    return pattern_data['entities']

# Preprocess the raw text data from user
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)  # Allow spaces
    return text.strip()

# Retrieve the best matching intent based on fuzzy matching
def get_intents(text, intents_list, threshold=75):
    text = preprocess(text)
    match = process.extractOne(text, intents_list)
    try:
        if match and match[1] >= threshold:
            return match[0], match[1]  # Return the matched intent and its score
        return None, 0
    except Exception as e:
        print(f"Exception: {e}")
        return None, 0

# Extract entities based on regex patterns
def entity_extractor(text, patterns):
    entities = {}
    for entity, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entities[entity] = match.group()
                break  # Stop after the first match
    return entities

# Process the user query to recognize intent and entities
def process_query(text, intents_list, patterns):
    entities = entity_extractor(text, patterns)
    intent, score = get_intents(text, intents_list)

    if score >= 80:
        return {
            'intent': intent,
            'entities': entities,
        }
    else:
        print("Could not understand query")
        return {
            "intent": intent,
            "entities": entities,
        }

# Main execution
if __name__ == "__main__":
    # Load intents and patterns
    intents_list = load_intents("../data/intent.json")
    patterns = load_patterns("../data/entity.json")

    # Example query
    query = "Good morning, what is the weather like today?"
    result = process_query(query, intents_list, patterns)
    print(result)