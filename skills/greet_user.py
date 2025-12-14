import random, datetime

def greet_user(query):
    query = query.lower()
    keys = ["hello", "hey", "hii", "hi"]
    greetings = [
        "Hello! How can I help you today?",
        "Hi there! What can I do for you?",
        "Welcome back! How may I assist you?",
        "Hey! I'm here whenever you need me.",
        "Hi! Ready when you are.",

        "Hey! Nice to see you again.",
        "Yo! What’s the plan today?",
        "Hey there! Need something?",
        "Hi! What’s on your mind?",

        "Greetings! How may I assist you today?",
        "Hello, I’m ready to support you. What would you like to do?",
        "Welcome! Please tell me how I can help.",
        "Your assistant is online. What task should I begin?",

        "Hey! Ready to make things happen?",
        "Hi! Let’s get started!",
        "Hello! I’m all set—what’s next?",
        "Great to see you! How can I help today?",

        "Hello! I’m analyzing your environment… just kidding. How can I help?",
        "Hi! Your virtual assistant is at your service.",
        "Hello! Optimizing myself for productivity. What do you need?",
        "Hi! I'm here and ready to assist with anything you need."
    ]

    if any(key in query for key in keys):
        return random.choice(greetings)

    else:
        return None


if __name__ == "__main__":
    print(greet_user("hello"))
    print(greet_user("hey"))
    print(greet_user("hii"))
    print(greet_user("hi"))
