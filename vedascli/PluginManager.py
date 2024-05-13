import importlib
import os
from collections import defaultdict
import builtins
import sys

class PluginManager:
    def __init__(self):
        self.plugin_dirs = []
        self.blacklisted_dirs = []
        self.plugins = {}
        self.dependencies = defaultdict(list)

    def _patch_import_exceptions(self):
        """
        Patch ImportError exceptions to include plugin name.
        """
        def import_hook(name, *args, **kwargs):
            try:
                return original_import(name, *args, **kwargs)
            except ImportError as e:
                raise ImportError(f"Error importing plugin '{name}': {e}")

        original_import = __import__
        builtins.__import__ = import_hook

    def add_directory(self, dir_path):
        """
        Add a directory to search for plugins.
        """
        if os.path.isdir(dir_path):
            self.plugin_dirs.append(dir_path)
        else:
            raise ValueError(f"'{dir_path}' is not a valid directory.")

    def add_blacklisted_directory(self, dir_path):
        """
        Add a directory to blacklist plugins from.
        """
        if os.path.isdir(dir_path):
            self.blacklisted_dirs.append(dir_path)
        else:
            raise ValueError(f"'{dir_path}' is not a valid directory.")

    def load_plugins(self):
        """
        Load plugins from all specified directories except blacklisted ones.
        """
        for plugin_dir in self.plugin_dirs:
            if plugin_dir not in self.blacklisted_dirs:
                for plugin_file in os.listdir(plugin_dir):
                    if plugin_file.endswith('.py') and plugin_file != "__init__.py":
                        plugin_name = os.path.splitext(plugin_file)[0]
                        self.load_plugin(plugin_name)

    def load_plugin(self, plugin_name):
        """
        Load a single plugin.
        """
        try:
            if plugin_name in self.plugins:
                self.unload_plugin(plugin_name)
            for plugin_dir in self.plugin_dirs:
                if plugin_dir not in self.blacklisted_dirs:
                    plugin_module = importlib.import_module(f"{plugin_dir}.{plugin_name}")
                    if hasattr(plugin_module, 'Plugin'):
                        plugin = plugin_module.Plugin()
                        dependencies = getattr(plugin, 'dependencies', [])
                        for dependency in dependencies:
                            self.dependencies[plugin_name].append(dependency)
                            self.load_plugin(dependency)
                        if self.check_dependencies(plugin_name):
                            self.plugins[plugin_name] = plugin
                            if hasattr(plugin, 'initialize'):
                                plugin.initialize()
                            # print(f"Plugin '{plugin_name}' loaded successfully.")
                        else:
                            print(f"Failed to load plugin '{plugin_name}' due to missing dependencies.")
                    else:
                        print(f"Plugin '{plugin_name}' does not contain a 'Plugin' class.")
        except Exception as e:
            print(f"Error loading plugin '{plugin_name}': {e}")

    def unload_plugin(self, plugin_name):
        """
        Unload a plugin.
        """
        if plugin_name in self.plugins:
            plugin = self.plugins.pop(plugin_name)
            if hasattr(plugin, 'cleanup'):
                plugin.cleanup()
            print(f"Plugin '{plugin_name}' unloaded successfully.")
        else:
            print(f"Plugin '{plugin_name}' is not loaded.")

    def execute_plugin(self, query):
        """
        Execute a plugin based on a query.
        """
        plugin_name = self.find_plugin_for_query(query)
        if plugin_name:
            self.run_plugin(plugin_name)
        else:
            print("No suitable plugin found for the query.")

    def reload_plugin(self, plugin_name):
        """
        Reload a plugin.
        """
        if plugin_name in self.plugins:
            self.unload_plugin(plugin_name)
            self.load_plugin(plugin_name)
        else:
            print(f"Plugin '{plugin_name}' is not loaded.")

    def run_plugin(self, plugin_name):
        """
        Run a loaded plugin.
        """
        if plugin_name in self.plugins:
            # print(f"Running plugin '{plugin_name}'...")
            self.plugins[plugin_name].run(self)
        # else:
        #     print(f"Plugin '{plugin_name}' is not loaded.")

    def list_plugins(self):
        """
        List loaded plugins.
        """
        print("Loaded plugins:")
        for plugin_name in self.plugins:
            print(plugin_name)

    def check_dependencies(self, plugin_name):
        """
        Check if all dependencies of a plugin are loaded.
        """
        for dependency in self.dependencies[plugin_name]:
            if dependency not in self.plugins:
                return False
        return True

    def find_plugin_for_query(self, query):
        """
        Find the most suitable plugin for a given query.
        """
        for plugin_name, plugin in self.plugins.items():
            if hasattr(plugin, 'matches_query') and plugin.matches_query(query):
                return plugin_name
        return None

    def add_plugin(self, plugin_name, plugin_object):
        """
        Manually add a plugin.
        """
        self.plugins[plugin_name] = plugin_object

    def lazy_load(self, plugin_name):
        """
        Load a plugin lazily.
        """
        if plugin_name not in self.plugins:
            self.load_plugin(plugin_name)

    def collect_plugins(self):
        """
        Collect loaded plugins.
        """
        return list(self.plugins.values())

    def validate_plugins(self):
        """
        Validate loaded plugins.
        """
        for plugin_name, plugin in self.plugins.items():
            if not hasattr(plugin, 'run'):
                print(f"Plugin '{plugin_name}' does not have a 'run' method.")

    def filter_duplicated_disabled(self):
        """
        Filter out duplicated and disabled plugins.
        """
        unique_plugins = {}
        for plugin_name, plugin in self.plugins.items():
            if plugin_name not in unique_plugins and getattr(plugin, 'enabled', True):
                unique_plugins[plugin_name] = plugin
        self.plugins = unique_plugins
        return self.plugins

    def get_plugins(self):
        """
        Get all loaded plugins.
        """
        return self.plugins

    def get_disabled(self):
        """
        Get disabled plugins.
        """
        disabled_plugins = {}
        for plugin_name, plugin in self.plugins.items():
            if not getattr(plugin, 'enabled', True):
                disabled_plugins[plugin_name] = plugin
        return disabled_plugins

    def get_number_plugins_loaded(self):
        """
        Get the number of loaded plugins.
        """
        return len(self.plugins)
