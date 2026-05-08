from google import genai

def init_client(api_key):
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, str(e)

def init_chat(client):
    try:
        return client.chats.create(model="gemini-2.0-flash"), None
    except Exception as e:
        return None, str(e)

def generate_text_stream(chat_session, prompt):
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            yield chunk.text
    except Exception as e:
        yield f"Ошибка: {str(e)}"
