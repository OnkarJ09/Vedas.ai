from vedascli.data.config import apikey
from vedascli.plugins.audio import say
from vedascli.utilities.lang_ids_for_recognizer import recognizer_lang_ids
import openai


class NoResponseException(Exception):
    pass


chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
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
        say(response["choices"][0]["text"],  str(recognizer_lang_ids))
        chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]
    except NoResponseException:
        say("try again", str(recognizer_lang_ids()))
        print("Try Again...")
        raise NoResponseException("No response from AI...")

