from google import genai

def init_chat_session(api_key):
    try:
        client = genai.Client(api_key=api_key)
        # We start a chat session with gemini-2.0-flash
        chat = client.chats.create(model="gemini-2.0-flash")
        return client, chat
    except Exception as e:
        return None, None

def generate_text_stream(chat_session, prompt):
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Произошла ошибка при обращении к Gemini: {str(e)}"
