"""
Nova Plugin Manager: Loads and runs plugins for calendar, weather, smart home, etc.
"""

import importlib
import os
import yaml

PLUGIN_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "plugins_config.yaml")

class NovaPluginManager:
    def __init__(self):
        self.plugins = []
        self.config = self.load_config()
        self.load_plugins()

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r") as f:
                    return yaml.safe_load(f)
            except Exception as e:
                print(f"Failed to load plugin config: {e}")
                return {}
        return {}

    def load_plugins(self):
        for fname in os.listdir(PLUGIN_DIR):
            if fname.endswith(".py") and fname != "plugin_manager.py":
                mod_name = fname[:-3]
                try:
                    mod = importlib.import_module(f"nova.plugins.{mod_name}")
                    self.plugins.append(mod)
                except Exception as e:
                    print(f"Failed to load plugin {mod_name}: {e}")

    def run_all(self, context):
        # Merge config into context for plugins
        merged_context = {**self.config, **context}
        results = {}
        for plugin in self.plugins:
            try:
                results[plugin.__name__] = plugin.run(merged_context)
            except Exception as e:
                results[plugin.__name__] = f"Error: {e}"
        return results
