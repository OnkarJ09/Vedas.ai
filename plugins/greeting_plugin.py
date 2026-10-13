from manager.env_manager import DEFAULT_USER
import datetime
import random


class Vedas:
    def __init__(self, config=None, **kwargs):
        self.name = "greeting_plugin"
        self.description = "Handles greetings like hello, hi, hey there, etc."
        self.parameters = ["input_data"]

        self.keywords = [
            "hello", "hey", "hii", "hi",
            "morning", "afternoon", "evening", "night",
            "how are you", "how are u", "how's it going"
        ]

        self.dependencies = []
        self.tool_map = {}
        self.config = config or {}
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
            "Hello, I’m ready to support you.",
            "Welcome! Please tell me how I can help.",

            "Hey! Ready to make things happen?",
            "Hi! Let’s get started!",
            "Hello! I’m all set—what’s next?",
            "Great to see you! How can I help today?"
        ]

    def matches_query(self, query):
        self.last_query = query.lower()
        return any(keyword in self.last_query for keyword in self.keywords)

    def run(self, input_data=None, state=None, **kwargs):
        print(f"[{self.name}] received:", input_data)

        query = (self.last_query or input_data or "").lower()
        clean_query = query.strip().lower()

        # Handle 'how are you' variations directly
        if any(p in clean_query for p in ["how are you", "how are u", "how's it going", "how is it going"]):
            return f"I'm doing great, {DEFAULT_USER}! Ready to help. What's on your mind?"

        if clean_query in ["hi", "hello", "hey", "heyy", "hii"]:
            return f"{DEFAULT_USER} {self.greet()} {random.choice(self.greetings)}"

        if any(clean_query.startswith(k + " ") for k in ["hi", "hello", "hey", "heyy", "hii"]):
            return f"{DEFAULT_USER} {self.greet()} {random.choice(self.greetings)}"

        return None

    def greet(self):
        # Time-based greeting
        hour = datetime.datetime.now().hour

        if 0 <= hour < 12:
            return "Good morning"
        elif 12 <= hour < 17:
            return "Good afternoon"
        elif 17 <= hour < 20:
            return "Good evening"
        else:
            return "Good night"

    def __str__(self):
        return f"{self.name} ({self.keywords})"