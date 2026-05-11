from anthropic import Anthropic
from dotenv import load_dotenv
import os
load_dotenv()
client = Anthropic()
with client.messages.stream(
              model=os.getenv("MODEL"),
              max_tokens=300,
              messages=[{"role": "user", "content": "10 sentence description about a fake database"}]) as stream:
    for text in stream.text_stream:
       pass

    print(stream.get_final_text())
