from vedascli.data.config import Vedas
import openai
import os


class NoResponse(Exception):
    pass


class Test_Vedas:
    def test___init__(self, **kwargs):
        self.keywords = ["Artificial Intelligence"]
        self.dependencies = []
        self.enabled = True
        self.last_query = None

    def test_match_query(self, query):
        query = query.replace("using", '')
        query = query.replace("artificial", '')
        query = query.replace("intelligence", '')
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def test_run(self, *args, **kwargs):
        if self.last_query:
            query_lower = self.last_query.lower()
            self.test_ai(query_lower)

    dependencies = ["test_config"]

    def test_ai(self, prompt):
        openai.api_key = Vedas.self.apikey
        text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # todo: Wrap this inside of a  try catch block
        # print(response["choices"][0]["text"])
        try:
            text += response["choices"][0]["text"]
        except NoResponse:
            raise NoResponse("AI didn't understand what you said")

        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
        with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
            f.write(text)
