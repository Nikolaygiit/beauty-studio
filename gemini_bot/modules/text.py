from google import genai
from google.genai import types

def get_chat_session(api_key):
    """
    Инициализирует сессию чата Gemini.
    Возвращает кортеж: (client, chat_session, error_message).
    Если произошла ошибка, первые два элемента будут None.
    """
    try:
        client = genai.Client(api_key=api_key)
        chat = client.chats.create(
            model="gemini-2.0-flash",
        )
        return client, chat, None
    except Exception as e:
        return None, None, f"Ошибка инициализации Gemini: {e}"

def generate_text(chat_session, prompt):
    """
    Отправляет текстовый запрос в сессию чата и возвращает ответ.
    Возвращает строку-ответ генератора или сообщение об ошибке.
    """
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Произошла ошибка при генерации текста: {e}"
