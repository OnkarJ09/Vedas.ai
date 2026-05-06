class AgentState:
    def __init__(self, query):
        self.query = query
        self.memory = {}
        self.results = {}
        self.last_output = None