from google import genai
from google.genai import types

def init_chat_session(api_key: str):
    """
    Инициализирует сессию чата Gemini с системными инструкциями на русском.
    Возвращает (client, chat_session).
    """
    client = genai.Client(api_key=api_key)

    # Настраиваем системные инструкции
    config = types.GenerateContentConfig(
        system_instruction="Ты — дружелюбный и полезный ИИ-помощник. Всегда отвечай на русском языке."
    )

    # Инициализируем историю чата
    chat = client.chats.create(model="gemini-2.0-flash", config=config)

    return client, chat

def generate_text_stream(chat_session, prompt: str):
    """
    Генерирует ответ в потоковом режиме, используя сессию чата.
    Возвращает генератор текста.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Произошла ошибка при генерации текста: {e}"
