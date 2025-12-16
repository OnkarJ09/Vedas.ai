import random
import datetime


class Vedas:
    def __init__(self, **kwargs):
        # Greeting keywords
        self.keywords = [
            "hello", "hey", "hii", "hi",
            "morning", "afternoon", "evening", "night"
        ]

        self.dependencies = []
        self.enabled = True
        self.last_query = None

        self.greetings = [
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

            "Hi! Your virtual assistant is at your service.",
            "Hello! Optimizing myself for productivity. What do you need?"
        ]

    def matches_query(self, query):
        self.last_query = query.lower()
        return any(keyword in self.last_query for keyword in self.keywords)

    def run(self, *args, **kwargs):
        if not self.last_query:
            return None

        # If user says hi / hello etc.
        if any(k in self.last_query for k in ["hello", "hey", "hii", "hi"]):
            return random.choice(self.greetings)

        # Time-based greeting
        hour = datetime.datetime.now().hour

        if 0 <= hour < 12:
            return "Good morning!"
        elif 12 <= hour < 17:
            return "Good afternoon!"
        elif 17 <= hour < 20:
            return "Good evening!"
        else:
            return "Good night!"
