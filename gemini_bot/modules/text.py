from google import genai
from google.genai import types

def init_chat_session(api_key):
    """Инициализирует клиента Gemini и создает новую сессию чата."""
    try:
        client = genai.Client(api_key=api_key)
        # Инициализируем пустую историю чата
        chat = client.chats.create(model="gemini-2.0-flash")
        return client, chat
    except Exception as e:
        return None, f"Ошибка инициализации Gemini: {e}"

def generate_text_stream(chat_session, prompt):
    """Генерирует текст (потоково) через активную сессию."""
    try:
        response = chat_session.send_message_stream(prompt)
        return response, None
    except Exception as e:
        return None, f"Ошибка генерации текста: {e}"
