import datetime
import random


def get_time_based_greeting():
    hour = datetime.datetime.now().hour
    time_based_greetings = {
        "morning": [
            "Good morning! Hope your day is off to a great start.",
            "Morning! How can I assist you today?",
            "Rise and shine! What would you like to do?"
        ],
        "afternoon": [
            "Good afternoon! How may I help?",
            "Hi! Hope your day is going well. What can I do for you?",
            "Hello! Ready to help whenever you are."
        ],
        "evening": [
            "Good evening! How can I assist you tonight?",
            "Evening! What would you like me to do?",
            "Hello! Hope you had a good day. How may I help you now?"
        ],
        "night": [
            "Good night! Need anything before you rest?",
            "It's late — how can I help you?",
            "Hi! I'm still awake if you need me."
        ]
    }

    if 5 <= hour < 12:
        period = "morning"
    elif 12 <= hour < 17:
        period = "afternoon"
    elif 17 <= hour < 22:
        period = "evening"
    else:
        period = "night"

    return random.choice(time_based_greetings[period])


# if __name__ == "__main__":
#     print(get_time_based_greeting())