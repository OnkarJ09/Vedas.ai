class MemoryManager:
    def __init__(self):
        self.short_term_memory = []
        self.long_term_memory = []
        self.user_profile = {}

    def add_short_term_memory(self, role, content):
        self.short_term_memory.append({
            "role": role,
            "content": content
        })

        # Limit short-term memory to the last 10 interactions
        self.short_term_memory = self.short_term_memory[-10:]

    def add_long_term_memory(self, memory):
        self.long_term_memory.append(memory)

    def get_recent_context(self):
        return "\n".join(
            f"{memory['role']}: {memory['content']}"
            for memory in self.short_term_memory
        )

    def get_long_term_memory(self):
        return "\n".join(self.long_term_memory)

    def update_profile(self, key, value):
        self.user_profile[key] = value

    def get_profile(self):
        return self.user_profile

