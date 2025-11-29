import logging
from datetime import datetime

# basic logger setup
logging.basicConfig(
    filename="vedas.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



class VedasAssistant:
    def __init__(self, user_name):
        self.user_name = user_name
        self.is_running = True

        # map simple commands to methods
        self.commands = {
            "hello": self.cmd_hello,
            "time": self.cmd_time,
            "help": self.cmd_help,
            "exit": self.cmd_exit,
        }

    def handle(self, text):
        """
        Main entry: takes user text, decides what to do.
        """
        text = text.strip().lower()

        # optional "hey vedas" hotword
        if text.startswith("hey vedas"):
            text = text.replace("hey vedas", "", 1).strip()

        if not text:
            return "Say something like 'hello', 'time', or 'help'."

        # pick command
        func = self.commands.get(text)
        if func:
            logging.info(f"Command received: {text}")
            return func()
        else:
            logging.warning(f"Unknown command: {text}")
            return "I didn't get that yet. Type 'help' to see options."

    # ------------- command methods -------------

    def cmd_hello(self):
        # TODO: return a hybrid-style greeting
        return f"Hey {self.user_name}! VEDAS online. Ready when you are. 😎"

    def cmd_time(self):
        # TODO: return current time nicely formatted
        now = datetime.now().strftime("%H:%M:%S")
        return f"Current time is {now}."

    def cmd_help(self):
        # TODO: show basic commands
        return (
            "Commands you can try:\n"
            "- hello : Greet\n"
            "- time  : Show current time\n"
            "- help  : Show this help\n"
            "- exit  : Quit VEDAS\n"
            "You can also start with 'Hey Vedas ...'"
        )

    def cmd_exit(self):
        self.is_running = False
        return "Shutting down. See you soon 👋"



if __name__ == "__main__":
    user_name = "Onkar"  # or input("Enter your name: ")

    vedas = VedasAssistant(user_name)
    print(f"Hello {user_name}, VEDAS online. Type 'help' to begin.\n")

    while vedas.is_running:
        user_input = input("You: ")
        reply = vedas.handle(user_input)
        print(f"VEDAS: {reply}")

