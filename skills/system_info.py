import platform


class Vedas:
    def __init__(self, **kwargs):
        self.keywords = [
            "system", "info", "information", "python",
            "version", "ver", "vr", "py", "sys"
        ]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    def matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def run(self, *args, **kwargs):

        if "system" in self.last_query and ("info" in self.last_query or "information" in self.last_query):
            return f"Running on {platform.system()} {platform.release()}"

        elif "python" in self.last_query and ("version" in self.last_query or
                                              "ver" in self.last_query or "vr" in self.last_query):
            return f"Running on Python {platform.python_version()}"

        else:
            return None






if __name__ == "__main__":
    print(system_info("system info"))
    print(system_info("python version"))
