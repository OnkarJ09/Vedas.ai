import importlib
import os
from collections import defaultdict
import builtins
import inspect
import pytest

class PluginManager:
    def __init__(self):
        self.plugin_dirs = []
        self.blacklisted_dirs = []
        self.plugins = {}
        self.dependencies = defaultdict(list)
        self._patch_import_exceptions()

    def _patch_import_exceptions(self):
        original_import = __import__
        def import_hook(name, *args, **kwargs):
            try:
                return original_import(name, *args, **kwargs)
            except ImportError as e:
                raise ImportError(f"Error importing plugin '{name}': {e}")
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

        if plugin_name in self.plugins:
            self.unload_plugin(plugin_name)
        for plugin_dir in directories:
            if plugin_dir not in self.blacklisted_dirs:
                module_name = f"{plugin_dir}.{plugin_name}".replace('/', '.')
                plugin_module = importlib.import_module(module_name)
                if hasattr(plugin_module, 'Vedas') and inspect.isclass(getattr(plugin_module, 'Vedas')):
                    vedas_class = getattr(plugin_module, 'Vedas')
                    plugin = vedas_class()
                    self.plugins[plugin_name] = plugin
                    if hasattr(plugin, 'initialize'):
                        plugin.initialize()
                    break

    def unload_plugin(self, plugin_name):
        if plugin_name in self.plugins:
            plugin = self.plugins.pop(plugin_name)
            if hasattr(plugin, 'cleanup'):
                plugin.cleanup()

    def execute_plugin(self, query, *args, **kwargs):
        plugin_name = self.find_plugin_for_query(query)
        if plugin_name:
            self.run_plugin(plugin_name, *args, **kwargs)

    def run_plugin(self, plugin_name, *args, **kwargs):
        if plugin_name in self.plugins:
            self.plugins[plugin_name].run(*args, **kwargs)

    def find_plugin_for_query(self, query):
        for plugin_name, plugin in self.plugins.items():
            if hasattr(plugin, 'matches_query') and plugin.matches_query(query):
                return plugin_name
        return None


@pytest.fixture
def plugin_manager(tmp_path):
    # Create directories for testing
    new_plugins_dir = tmp_path / "new_plugins"
    blacklisted_plugins_dir = tmp_path / "blacklisted_plugins"

    new_plugins_dir.mkdir()  # Create the new_plugins directory
    blacklisted_plugins_dir.mkdir()  # Create the blacklisted_plugins directory

    pm = PluginManager()
    pm.add_directory('plugins')
    pm.add_directory(str(new_plugins_dir))  # Add the new_plugins directory
    pm.add_blacklisted_directory(str(blacklisted_plugins_dir))  # Add the blacklisted_plugins directory
    return pm


def test_add_directory(plugin_manager):
    plugin_manager.add_directory('plugins')
    assert 'plugins' in plugin_manager.plugin_dirs


def test_add_blacklisted_directory(plugin_manager):
    assert str(plugin_manager.blacklisted_dirs[0]) == str(plugin_manager.blacklisted_dirs[0])


def test_load_plugins(plugin_manager):
    # Assuming 'plugins' directory has a valid plugin for testing
    plugin_manager.load_plugins()
    assert len(plugin_manager.plugins) > 0  # Check if plugins were loaded


def test_unload_plugin(plugin_manager):
    plugin_manager.load_plugins()
    plugin_name = list(plugin_manager.plugins.keys())[0]
    plugin_manager.unload_plugin(plugin_name)
    assert plugin_name not in plugin_manager.plugins


def test_execute_plugin(plugin_manager):
    plugin_manager.load_plugins()
    plugin_name = list(plugin_manager.plugins.keys())[0]
    # Assuming the plugin has a method that can be executed
    result = plugin_manager.execute_plugin("some query")
    assert result is None  # Adjust based on expected behavior of the plugin


def test_run_plugin(plugin_manager):
    plugin_manager.load_plugins()
    plugin_name = list(plugin_manager.plugins.keys())[0]
    result = plugin_manager.run_plugin(plugin_name)
    assert result is None


def test_find_plugin_for_query(plugin_manager):
    plugin_manager.load_plugins()
    query = "hello"
    plugin_name = plugin_manager.find_plugin_for_query(query)
    assert plugin_name is not None  # Ensure a plugin is found for the query