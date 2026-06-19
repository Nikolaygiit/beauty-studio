from google import genai
from google.genai import types

def create_client(api_key: str):
    return genai.Client(api_key=api_key)

def create_chat_session(client, history=None):
    if history is None:
        history = []

    config = types.GenerateContentConfig(
        system_instruction="Всегда отвечай на русском языке.",
    )

    # In genai, history needs to be a list of Content objects
    # client.chats.create takes the model name
    return client.chats.create(
        model="gemini-2.0-flash",
        config=config,
    )
