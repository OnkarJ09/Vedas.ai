from task_manager.PluginManager import PluginManager
from plugins.audio import take_command
import sys


if __name__ == "__main__":
    # Instantiate the PluginManager
    plugin_manager = PluginManager()

    # Add the directories to search for plugins
    plugin_manager.add_directory("plugins")

    # Load all the plugins from the directory
    plugin_manager.load_plugins()

    # Default language is English
    current_language = "en"

    while True:
        query, language_changed = take_command(current_language)
        # query = input("Enter your query: ").lower()
        # language_changed = None

        if query is None:
            continue    # Repeat listening if the command wasn't understood

        if language_changed:
            current_language = query
            continue    # Skip further processing and start listening in new language

        if query == "exit":
            sys.exit(0)
        else:
            plugin_manager.execute_plugin(query)
