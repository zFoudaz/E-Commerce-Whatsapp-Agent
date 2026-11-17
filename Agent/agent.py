from google import genai
from config import settings
from google.genai import types
import prompts as prompts

client = genai.Client(api_key=settings.GEMINI_API_KEY)

config = types.GenerateContentConfig(
    system_instruction= prompts.SYSTEM_PROMPT
)

chat = client.chats.create(
    model=settings.GEMINI_MODEL,
    config=config
)

prompt = "hello can you introduce yourself"

response = chat.send_message(prompt)
print(response.text)