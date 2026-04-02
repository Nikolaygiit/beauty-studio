from google import genai
from google.genai import types

def init_chat_session(api_key):
    client = genai.Client(api_key=api_key)
    return client.chats.create(model="gemini-2.0-flash")

def get_gemini_response(chat_session, prompt):
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Произошла ошибка при генерации текста: {e}"
