"""
Removing the mcp-use...

Now using a custom framework and a custom manager to integrate the same behavior as the mcp-use!!!
"""
from manager.plugin_manager import PluginManager
from utlis.audio import take_command
import asyncio

"""
    To-Do:
    
    This is to be added to the manager to manage config/.env variables and secrets in a secure way,
    and to provide an interface for tools to access them without directly reading the .env file or
    using dotenv in the tools themselves.
    
    from manager.config_manager import ConfigManager
"""

if __name__ == "__main__":
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

    while True:
        # Execute plugins/tools based on user input/queries
        query = asyncio.run(take_command())
        plugin_manager.execute_pipeline(query)
