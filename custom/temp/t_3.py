import importlib
import os
from collections import defaultdict
import builtins
import inspect

class PluginManager:
    def __init__(self):
        self.plugin_dirs = []
        self.blacklisted_dirs = []
        self.plugins = {}
        self.dependencies = defaultdict(list)
        self._patch_import_exceptions()

    def _patch_import_exceptions(self):
        def import_hook(name, *args, **kwargs):
            try:
                return original_import(name, *args, **kwargs)
            except ImportError as e:
                raise ImportError(f"Error importing plugin '{name}': {e}")

        original_import = __import__
        builtins.__import__ = import_hook

    def add_directory(self, dir_path):
        if os.path.isdir(dir_path):
            self.plugin_dirs.append(dir_path)
        else:
            raise ValueError(f"'{dir_path}' is not a valid directory.")

    def add_blacklisted_directory(self, dir_path):
        if os.path.isdir(dir_path):
            self.blacklisted_dirs.append(dir_path)
        else:
            raise ValueError(f"'{dir_path}' is not a valid directory.")

    def load_plugins(self):
        for plugin_dir in self.plugin_dirs:
            if plugin_dir not in self.blacklisted_dirs:
                for plugin_file in os.listdir(plugin_dir):
                    if plugin_file.endswith('.py') and plugin_file != "__init__.py":
                        plugin_name = os.path.splitext(plugin_file)[0]
                        self.load_plugin(plugin_name, [plugin_dir])

    def load_plugin(self, plugin_name, directories=None):
        directories = directories or self.plugin_dirs

        try:
            if plugin_name in self.plugins:
                self.unload_plugin(plugin_name)
            for plugin_dir in directories:
                if plugin_dir not in self.blacklisted_dirs:
                    module_name = f"{plugin_dir}.{plugin_name}".replace('/', '.')
                    plugin_module = importlib.import_module(module_name)
                    if hasattr(plugin_module, 'Vedas') and inspect.isclass(getattr(plugin_module, 'Vedas')):
                        vedas_class = getattr(plugin_module, 'Vedas')
                        plugin = vedas_class()
                        dependencies = getattr(plugin, 'dependencies', [])
                        for dependency in dependencies:
                            self.dependencies[plugin_name].append(dependency)
                            self.load_plugin(dependency, directories)
                        if self.check_dependencies(plugin_name):
                            self.plugins[plugin_name] = plugin
                            if hasattr(plugin, 'initialize'):
                                plugin.initialize()
                            print(f"Plugin '{plugin_name}' loaded successfully.")
                        else:
                            print(f"Failed to load plugin '{plugin_name}' due to missing dependencies.")
                        break
                    else:
                        print(f"Plugin '{plugin_name}' does not contain a 'Vedas' class or it's not a class.")
        except Exception as e:
            print(f"Error loading plugin '{plugin_name}': {e}")

    def unload_plugin(self, plugin_name):
        if plugin_name in self.plugins:
            plugin = self.plugins.pop(plugin_name)
            if hasattr(plugin, 'cleanup'):
                plugin.cleanup()
            print(f"Plugin '{plugin_name}' unloaded successfully.")
        else:
            print(f"Plugin '{plugin_name}' is not loaded.")

    def execute_plugin(self, query, *args, **kwargs):
        plugin_name = self.find_plugin_for_query(query)
        if plugin_name:
            print(f"Executing plugin '{plugin_name}' for query: {query}")
            self.run_plugin(plugin_name, *args, **kwargs)
        else:
            print("No suitable plugin found for the query.")

    def reload_plugin(self, plugin_name):
        if plugin_name in self.plugins:
            self.unload_plugin(plugin_name)
            self.load_plugin(plugin_name)
        else:
            print(f"Plugin '{plugin_name}' is not loaded.")

    def run_plugin(self, plugin_name, *args, **kwargs):
        if plugin_name in self.plugins:
            print(f"Running plugin '{plugin_name}'...")
            self.plugins[plugin_name].run(*args, **kwargs)
        else:
            print(f"Plugin '{plugin_name}' is not loaded.")

    def list_plugins(self):
        print("Loaded plugins:")
        for plugin_name in self.plugins:
            print(plugin_name)

    def check_dependencies(self, plugin_name):
        for dependency in self.dependencies[plugin_name]:
            if dependency not in self.plugins:
                return False
        return True

    def find_plugin_for_query(self, query):
        for plugin_name, plugin in self.plugins.items():
            if hasattr(plugin, 'matches_query') and plugin.matches_query(query):
                return plugin_name
        return None

    def add_plugin(self, plugin_name, plugin_object):
        self.plugins[plugin_name] = plugin_object

    def lazy_load(self, plugin_name):
        if plugin_name not in self.plugins:
            self.load_plugin(plugin_name)

    def collect_plugins(self):
        return list(self.plugins.values())

    def validate_plugins(self):
        for plugin_name, plugin in self.plugins.items():
            if not hasattr(plugin, 'run'):
                print(f"Plugin '{plugin_name}' does not have a 'run' method.")

    def filter_duplicated_disabled(self):
        unique_plugins = {}
        for plugin_name, plugin in self.plugins.items():
            if plugin_name not in unique_plugins and getattr(plugin, 'enabled', True):
                unique_plugins[plugin_name] = plugin
        self.plugins = unique_plugins
        return self.plugins

    def get_plugins(self):
        return self.plugins

    def get_disabled(self):
        disabled_plugins = {}
        for plugin_name, plugin in self.plugins.items():
            if not getattr(plugin, 'enabled', True):
                disabled_plugins[plugin_name] = plugin
        return disabled_plugins

    def get_number_plugins_loaded(self):
        return len(self.plugins)

if __name__ == "__main__":
    # Example usage
    plugin_manager = PluginManager()

    # Add plugin directories
    plugin_manager.add_directory('scrap')

    # Load all plugins from the specified directories
    plugin_manager.load_plugins()

    # List loaded plugins
    plugin_manager.list_plugins()

    while True:
        # Execute a plugin based on a query
        query = input("Enter a query: ")
        plugin_manager.execute_plugin(query)
