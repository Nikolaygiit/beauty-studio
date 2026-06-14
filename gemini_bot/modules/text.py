from google import genai
from google.genai import types

def setup_chat_session(api_key: str):
    """Sets up the Gemini chat session and returns the client and session."""
    client = genai.Client(api_key=api_key)

    config = types.GenerateContentConfig(
        system_instruction="Always respond in Russian.",
    )

    chat_session = client.chats.create(model='gemini-2.0-flash', config=config)

    return client, chat_session
