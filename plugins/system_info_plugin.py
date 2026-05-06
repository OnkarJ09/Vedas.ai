import platform


class Vedas:
    def __init__(self, config=None, **kwargs):
        self.name = "system_info_plugin"
        self.description = "Provides system information like OS details and Python version"
        self.parameters = ["input_data"]

        self.keywords = [
            "system", "info", "information",
            "python", "version", "ver", "py", "sys"
        ]

        self.dependencies = []
        self.tool_map = {}
        self.config = config or {}
        self.enabled = True
        self.last_query = None

    def matches_query(self, query):
        self.last_query = query.lower()
        return any(keyword in self.last_query for keyword in self.keywords)

    def run(self, input_data=None, state=None, **kwargs):
        print(f"[{self.name}] received:", input_data)

        # Determine query source (important for LLM + chaining)
        query = (self.last_query or input_data or "").lower()

        # System info
        if "system" in query and ("info" in query or "information" in query):
            return f"Running on {platform.system()} {platform.release()}"

        # Python version
        elif "python" in query and ("version" in query or "ver" in query):
            return f"Running on Python {platform.python_version()}"

        # Fallback (VERY IMPORTANT)
        return f"System: {platform.system()} {platform.release()} | Python: {platform.python_version()}"

    def __str__(self):
        return f"{self.name} ({self.keywords})"