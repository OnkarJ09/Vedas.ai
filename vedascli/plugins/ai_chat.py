from vedascli.data.config import Vedas
from .audio import say
from vedascli.utilities.lang_ids_for_recognizer import Vedas
import openai


class NoResponseException(Exception):
    pass


class Vedas:
    def __init__(self, **kwargs):
        self.apikey = Vedas.self.apikey
        self.dependencies = ["audio", "config"]
        self.last_query = None
        self.enabled = True

    def matches_query(self, query):
        self.last_query = query
        return query

    # This wil help run the chat with vedas_ai using VedasPluginManager
    def run(self, *args, **kwargs):
        if self.last_query:
            query = self.last_query
            if query:
                self.chat(query)

    dependencies = ["audio"]

    #  To chat with vedas_ai
    def chat(self, query):
        """
        Chat with vedas_ai
        It uses openai api to chat with vedas_ai in background
        """
        chatStr = ""
        openai.api_key = self.apikey
        chatStr += f"You: {query}\n Vedas_ai: "
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        try:
            say(response["choices"][0]["text"])
            chatStr += f"{response['choices'][0]['text']}\n"
            return response["choices"][0]["text"]
        except NoResponseException:
            say("try again", )
            print("Try Again...")
            raise NoResponseException("No response from AI...")
