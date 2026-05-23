"""
Removing the mcp-use...

Now using a custom framework and a custom manager to integrate the same behavior as the mcp-use!!!
"""
import sys

from manager.plugin_manager import PluginManager
from manager.env_manager import DEFAULT_LANGUAGE_CODE, DEFAULT_VOICE
from utlis.audio import take_command, say
import asyncio

"""
    To-Do:
    
    This is to be added to the manager to manage config/.env variables and secrets in a secure way,
    and to provide an interface for tools to access them without directly reading the .env file or
    using dotenv in the tools themselves.
    
    from manager.config_manager import ConfigManager
"""

async def main():

    # Initialize the plugin manager
    plugin_manager = PluginManager()

    # Load directories
    plugin_manager.add_directory("plugins")
    # print("[DEBUG] tool_map =", plugin_manager.tool_map)      # For debugging

    # Load plugins (tools)
    plugin_manager.load_plugins()

    # For debugging: print loaded tools
    print("[DEBUG] Loaded tools:")
    plugin_manager.list_plugins()

    # Current language
    current_language = DEFAULT_LANGUAGE_CODE
    current_voice = DEFAULT_VOICE

    while True:
        # Execute plugins/tools based on user input/queries
        # query, language_changed, new_lang_and_voice = take_command(current_language)
        query, language_changed, new_lang_and_voice = await take_command(current_language)

        # Handle empty query
        if query is None:
            continue

        # Change the language and the voice when user asks to change the language
        if language_changed:
            current_language = new_lang_and_voice[0]    # Get the language code for Recognizer
            current_voice = new_lang_and_voice[1]       # Get the voice name for TTS

        # Exit the system
        if query == "exit":
            print("Exiting...")
            sys.exit(0)

        # Execute plugin pipeline for other queries
        else:
            response = plugin_manager.execute_pipeline(query)
            await say(str(response), current_voice)


if __name__ == "__main__":
    asyncio.run(main())