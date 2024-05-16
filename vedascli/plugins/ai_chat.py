from vedascli.data.config import apikey
from vedascli.plugins.audio import Plugin
from vedascli.utilities.lang_ids_for_recognizer import Plugin
import openai


class NoResponseException(Exception):
    pass


class Plugin:
    # This wil help run the chat with vedas_ai using PluginManager
    def run(self, *args, **kwargs):
        query = kwargs.get("query")
        if query:
            chat(query)

        dependencies = ["audio"]

# To chat with vedas_ai
def chat(query):
    """
    Chat with vedas_ai
    It uses openai api to chat with vedas_ai in background
    """
    chatStr = ""
    openai.api_key = apikey
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
        Plugin.say(response["choices"][0]["text"])
        chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]
    except NoResponseException:
        Plugin.say("try again", )
        print("Try Again...")
        raise NoResponseException("No response from AI...")
