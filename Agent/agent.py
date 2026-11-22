from google import genai
from Agent.config import settings
from google.genai import types
import Agent.prompts as prompts
from Agent.tools import tools
import json

client = genai.Client(api_key=settings.GEMINI_API_KEY)

config = types.GenerateContentConfig(
    system_instruction= prompts.SYSTEM_PROMPT,
    tools=tools,
    temperature=0
)

def create_chat(history = None):
    chat = client.chats.create(
        model=settings.GEMINI_MODEL,
        config=config,
        history= history
    )
    return chat

def send_message(chat, message):
    prompt = message
    return chat.send_message(prompt)


def dump_history(self) -> list[dict]:
    return [json.loads(c.model_dump_json(exclude_none=True)) for c in self.get_history()]

if __name__ == '__main__':
    chat = create_chat()
    print(send_message(chat,'hello can you introduce yourself and list the tools you have?'))