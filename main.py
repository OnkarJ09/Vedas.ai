from skills import *
import logging, dotenv

# ---------------- LOGGER SETUP ---------------- #
logger = logging.getLogger("VEDAS")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("vedas.log", mode="a")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# ---------------- VEDAS CORE ---------------- #
if __name__ == "__main__":
    get_time_based_greeting()

    while True:
        query = input("User -> ").lower()

        if query == "exit":
            break




