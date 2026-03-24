from google import genai

def get_gemini_client(api_key):
    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        return None

def initialize_chat(client):
    try:
        return client.chats.create(model="gemini-2.0-flash")
    except Exception as e:
        return None

def generate_text_stream(chat_session, prompt):
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Произошла ошибка при генерации текста: {e}"
