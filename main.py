from utils.greet_user_acc_time import get_time_based_greeting
from manager.plugin_manager import PluginManager
import logging
import tomllib


# ----------------  INITIALIZE ENVIRONMENT VARIABLE   -------------- #
with open("utils/config.toml", "rb") as f:
    env_var = tomllib.load(f)



# ---------------- LOGGER SETUP ---------------- #
logger = logging.getLogger("VEDAS")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("vedas.log", mode="a")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# ---------------- VEDAS CORE ---------------- #
if __name__ == "__main__":
    # initialize plugin manager
    plugin_manager = PluginManager()

    # define the plugin dir.
    plugin_manager.add_directory("skills")

    # load all the skills/plugins in dir with "Vedas" class
    plugin_manager.load_plugins()

    # greet user
    greet = get_time_based_greeting() + f" {env_var['username']}"
    print(greet)
    logger.info(f"Greeting with new session {env_var['username']}")

    while True:
        query = input("User -> ").lower()
        logger.info(f"User -> {query}")     # user query log..

        if query is None:
            continue

        if query == "exit":
            logger.info("Goodbye!!....")
            break

        elif query == "help":
            #TODO: add a help skill and implement it here or with plugin it self
            pass

        else:
            result = plugin_manager.execute_plugin(query)
            print(result)
            logger.info(f"VEDAS -> {result}")





