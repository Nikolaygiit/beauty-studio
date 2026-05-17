from google import genai

def init_chat_session(client, history=None):
    if history is None:
        history = []
    return client.chats.create(model="gemini-2.0-flash", config={"system_instruction": "You are a helpful and polite AI assistant. Always respond in Russian."})

def send_message_stream(chat_session, prompt):
    try:
        response = chat_session.send_message_stream(prompt)
        return response, None
    except Exception as e:
        return None, str(e)
