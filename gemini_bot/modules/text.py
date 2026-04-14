from google import genai

def init_gemini_client(api_key):
    """Инициализирует клиент Gemini и создает сессию чата."""
    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model="gemini-2.0-flash")
    return client, chat

def generate_text_stream(chat_session, prompt):
    """Генерирует текст в виде потока, обрабатывая возможные ошибки."""
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Произошла ошибка при генерации текста:** {str(e)}"
