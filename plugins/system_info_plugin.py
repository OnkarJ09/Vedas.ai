import platform


class Vedas:
    def __init__(self, config=None, **kwargs):
        self.name = "system_info_plugin"
        self.description = "Provides system information like OS details and Python version"
        self.parameters = ["input_data"]

        # Intent phrases for system/python info queries
        self.keywords = [
            "system info", "system information", "system specs", "system status",
            "os version", "operating system",
            "python version", "python ver", "which python"
        ]

        # Standalone queries
        self.standalone_words = ["system info", "sysinfo", "specs", "system"]

        self.dependencies = []
        self.tool_map = {}
        self.config = config or {}
        self.enabled = True
        self.last_query = None

    def matches_query(self, query):
        q = (query or "").strip().lower()
        self.last_query = q
        if q in self.standalone_words:
            return True
        return any(keyword in q for keyword in self.keywords)

    def run(self, input_data=None, state=None, **kwargs):
        print(f"[{self.name}] received:", input_data)

        query = (input_data or self.last_query or "").strip().lower()

        # Python version
        if any(p in query for p in ["python version", "python ver", "which python"]) or query == "python":
            return f"Running on Python {platform.python_version()}"

        # System info
        if any(p in query for p in ["system info", "system information", "system specs", "os version", "operating system"]) or query in self.standalone_words:
            return f"Running on {platform.system()} {platform.release()}"

        # General combination
        if "system" in query and ("info" in query or "spec" in query or "detail" in query):
            return f"System: {platform.system()} {platform.release()} | Python: {platform.python_version()}"

        # Return None so conversational queries fall back to LLM chat
        return None

    def __str__(self):
        return f"{self.name} ({self.keywords})"