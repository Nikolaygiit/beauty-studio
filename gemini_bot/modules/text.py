from google import genai

SYSTEM_INSTRUCTION = "You are a helpful assistant. Always respond in Russian."

def init_gemini_client(api_key: str):
    return genai.Client(api_key=api_key)

def init_chat_session(client, chat_history=None):
    if chat_history is None:
        chat_history = []

    # We are using gemini-2.0-flash
    config = {"system_instruction": SYSTEM_INSTRUCTION}

    return client.chats.create(
        model="gemini-2.0-flash",
        config=config,
    )
