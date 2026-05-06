from utlis.text_normalizer import normalize_text
from collections import defaultdict
from utlis.state import AgentState
from openai import OpenAI
import importlib
import builtins
import inspect
import dotenv
import os, re
import json

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=dotenv.get_key(".env", "OPENAI")
)


class PluginManager:
    def __init__(self):
        self.plugin_dirs = []
        self.blacklisted_dirs = []
        self.plugins = {}
        self.tool_map = {}
        self.dependencies = defaultdict(list)
        self._patch_import_exceptions()
        self.personality = "vedas"
        self.tone = "smart"

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
                            self.tool_map[plugin.name] = plugin_name
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

    def run_plugin(self, plugin_name, state, args=None, **kwargs):
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]

            print(f"[Vedas] Running plugin '{plugin_name}' with args:", args)

            # 🔥 FIX: support ANY key from LLM
            input_data = None

            if args:
                # try common keys
                input_data = (
                        args.get("input_data") or
                        args.get("input") or
                        args.get("message") or
                        args.get("query") or
                        next(iter(args.values()), None)  # fallback → first value
                )

            # final fallback
            if input_data is None:
                input_data = state.query

            result = plugin.run(
                input_data=input_data,
                state=state
            )

            state.results[plugin_name] = result
            state.last_output = result

            return result

    def shortlist_plugins(self, query):
        selected = []

        for name, plugin in self.plugins.items():
            if hasattr(plugin, "keywords"):
                if any(k in query.lower() for k in plugin.keywords):
                    selected.append(name)

        return selected

    def execute_pipeline(self, query):
        analysis = self.analyze_intent(query)

        cleaned_query = analysis["cleaned"]

        self.tone = analysis.get("tone", "smart")
        self.personality = analysis.get("personality", "vedas")

        print("[DEBUG] Normalized query:", cleaned_query)

        state = AgentState(cleaned_query)

        # ---------------------
        shortlisted_tools = self.shortlist_plugins(cleaned_query)
        if not shortlisted_tools:
            print("[Vedas] No matching tools found.")
            return "No suitable tools for query"

        print("[Vedas] Shortlisted:", shortlisted_tools)

        tools_meta = self.get_tools_metadata(shortlisted_tools)

        plan = self.get_plan_from_llm(cleaned_query, tools_meta)

        print("[Vedas] Plan:", plan)

        outputs = []

        for step in plan:
            tool_name = step["tool"]
            args = step.get("args", {})

            plugin_name = self.tool_map.get(tool_name)
            if not plugin_name:
                print(f"[ERROR] Tool '{tool_name}' not mapped")
                continue

            result = self.run_plugin(plugin_name, state, args)

            if result:
                outputs.append(result)

        print("[Vedas] Final output:", state.last_output)

        mode = self.decide_mode(cleaned_query, state, outputs)

        self.personality = mode.get("personality", "jarvis")
        self.tone = mode.get("tone", "smart")

        print("[DEBUG] Mode selected:", self.personality, "|", self.tone)

        final_output = self.synthesize_response(cleaned_query, outputs)

        print("\n[Vedas Response]")
        print("----------------")
        print(final_output)
        print("----------------\n")

        return final_output

    def safe_json_parse(self, text):
        try:
            return json.loads(text)
        except:
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return []

    def get_plan_from_llm(self, query, tools):
        tool_text = "\n".join(
            [f"{t['name']}: {t['description']}" for t in tools]
        )

        prompt = f"""
            You are an AI planner.

            User query:
            {query}

            Available tools:
            {tool_text}

            Return a JSON array of tools in execution order.

            Example:
            [
              {{"tool": "tool1", "args": {{"input_data": "example"}}}}
            ]

            ONLY return JSON.
        """

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{
                "role": "user",
                "content": f"{prompt}"
            }],
            temperature=0
        )

        content = response.choices[0].message.content

        try:
            return self.safe_json_parse(content)
        except:
            print("[ERROR] Invalid JSON from LLM:", content)
            return []

    def synthesize_response(self, query, outputs):
        if not outputs:
            return "I couldn't find a response."

        combined = "\n".join(outputs)

        personality_prompt = {
            "normal": "You are a helpful assistant.",
            "vedas": "You are VEDAS, a highly intelligent, calm, slightly witty AI assistant. Speak elegantly.",
            "casual": "You are a friendly, casual assistant. Keep things relaxed and fun.",

            # For FUN
            "sarcastic": "You are a sarcastic assistant. Be witty, slightly teasing, but not rude or offensive. Keep it clever.",
            "dark": "You are a dark-humor assistant. Your tone is dry, slightly grim, but still helpful and not harmful."
        }

        tone_prompt = {
            "formal": "Respond formally and professionally.",
            "casual": "Respond casually and conversationally.",
            "smart": "Respond naturally and intelligently.",

            # For FUN
            "sarcastic": "Add light sarcasm and wit in your tone.",
            "dark": "Add subtle dark humor but keep it safe and not disturbing."
        }

        system_prompt = f"""
            {personality_prompt.get(self.personality)}
            {tone_prompt.get(self.tone)}

            Rules:
            - Be natural and engaging
            - Do NOT be offensive, harmful, or abusive
            - Keep sarcasm playful, not toxic
            - Keep dark humor subtle, not disturbing
            - Combine tool outputs into ONE response
            - Do NOT list outputs separately
        """

        user_prompt = f"""
            User query:
            {query}

            Tool outputs:
            {combined}
        """

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # or your NVIDIA model later
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    def decide_mode(self, query, state, outputs):
        context = "\n".join(outputs)

        prompt = f"""
            You are an AI personality selector.

            User query:
            {query}

            Context (tool outputs):
            {context}

            Decide the BEST personality and tone for responding.

            Available personalities:
            - normal
            - vedas
            - casual
            - sarcastic
            - dark

            Available tones:
            - formal
            - casual
            - smart
            - sarcastic
            - dark

            Rules:
            - Be natural and context-aware
            - Use sarcastic only if user tone supports it
            - Use dark only if context allows subtle humor
            - Default to vedas if unsure

            Return ONLY JSON:
            {{
              "personality": "...",
              "tone": "..."
            }}
        """

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # or your NVIDIA model later
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        try:
            return json.loads(response.choices[0].message.content)
        except:
            return {"personality": "vedas", "tone": "smart"}

    def analyze_intent(self, raw_query):
        normalized_query = normalize_text(raw_query)

        prompt = f"""
            You are an AI input analyzer.

            User query:
            {raw_query}

            Tasks:
            1. Detect tone/style of user

            Return JSON ONLY:
            {{
                "tone": "..",
                "personality": "..."
            }}

            Possible tones:
            - formal
            - casual
            - sarcastic
            - dark
            - excited

            Possible personalities:
            - normal
            - vedas
            - casual
            - sarcastic
            - dark
        """

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=0
        )

        try:
            return json.loads(response.choices[0].message.content) + {
                "cleaned": f"{normalized_query: 'cleaned'}"
            }
        except:
            return {
                "cleaned": normalized_query,
                "tone": "smart",
                "personality": "vedas",
            }

    def get_tools_metadata(self, tool_names):
        tools = []

        for name in tool_names:
            plugin = self.plugins[name]
            tools.append({
                "name": plugin.name,
                "description": getattr(plugin, "description", "No description")
            })

        return tools

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

    def execute_plugin(self, query, *args, **kwargs):
        plugin_name = self.find_plugin_for_query(query)
        if plugin_name:
            print(f"Executing plugin '{plugin_name}' for query: {query}")
            return self.run_plugin(plugin_name, *args, **kwargs)
        else:
            print("No suitable plugin found for the query.")
            return None


    """
        Wrap the below as tools that can be helpful for resolving tool/plugins errors!!
    """
    def reload_plugin(self, plugin_name):
        if plugin_name in self.plugins:
            self.unload_plugin(plugin_name)
            self.load_plugin(plugin_name)
        else:
            print(f"Plugin '{plugin_name}' is not loaded.")

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
    plugin_manager.add_directory('servers')

    # Load all plugins from the specified directories
    plugin_manager.load_plugins()
    print("[DEBUG] tool_map =", plugin_manager.tool_map)

    # List loaded plugins
    plugin_manager.list_plugins()

    while True:
        # Execute a plugin based on a query
        query = input("Enter a query: ")
        plugin_manager.execute_pipeline(query)
