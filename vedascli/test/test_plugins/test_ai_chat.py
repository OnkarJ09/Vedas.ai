from vedascli.test.test_plugins.test_config import apikey
import openai
import pytest


@pytest.fixture(autouse=True)
def query():
    return "Vedas_ai"


class NoResponseException(Exception):
    pass


chatStr = ""
def test_chat(query):
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
        say(response["choices"][0]["text"])
        chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]
    except NoResponseException:
        print("Try Again...")
        raise NoResponseException("No response from AI...")

