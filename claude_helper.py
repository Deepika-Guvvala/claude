import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class ChatBot:
    def __init__(self, system_prompt=None, temperature = None, stop_sequences = None):
        self.client = Anthropic()
        self.model = os.getenv("MODEL")
        self.max_tokens = 1400
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.stop_sequences = stop_sequences
        self.messages = []

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content):
        self.messages.append({"role": "assistant", "content": content})

    def chat(self, message, prefill=None):
        self.add_user_message(message)
        if prefill:
            self.add_assistant_message(prefill)
        kwargs = dict(model=self.model, max_tokens=self.max_tokens, messages=self.messages, stop_sequences=self.stop_sequences)
        if self.system_prompt:
            kwargs["system"] = self.system_prompt
        if self.temperature:
            kwargs["temperature"] = self.temperature
        response = self.client.messages.create(**kwargs)
        reply = response.content[0].text
        if prefill:
            self.messages.pop()
            self.add_assistant_message(prefill + reply)
        else:
            self.add_assistant_message(reply)
        return reply
