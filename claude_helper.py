import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class ChatBot:
    def __init__(self, system_prompt=None):
        self.client = Anthropic()
        self.model = os.getenv("MODEL")
        self.max_tokens = 300
        self.system_prompt = system_prompt
        self.messages = []

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content):
        self.messages.append({"role": "assistant", "content": content})

    def chat(self, message):
        self.add_user_message(message)
        kwargs = dict(model=self.model, max_tokens=self.max_tokens, messages=self.messages)
        if self.system_prompt:
            kwargs["system"] = self.system_prompt
        response = self.client.messages.create(**kwargs)
        reply = response.content[0].text
        self.add_assistant_message(reply)
        return reply
