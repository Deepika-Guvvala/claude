from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
messages =[]
client = Anthropic()
model = "claude-haiku-4-5-20251001"
max_tokens = 300

def add_user_message(content):
    messages.append({"role": "user", "content": content})

def add_assistant_message(content):
    messages.append({"role": "assistant", "content": content})

def chat(message):
    add_user_message(message)
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
    )
    reply = response.content[0].text
    add_assistant_message(reply)
    return reply

while True:
    user_input = input("> ")
    print(chat(user_input))
