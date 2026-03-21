from google import genai

def get_gemini_client(api_key: str):
    """
    Инициализирует клиента Google GenAI с использованием нового пакета google-genai.
    """
    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        return f"Ошибка инициализации Gemini: {str(e)}"

def init_chat_session(client):
    """
    Создает новую сессию чата для генерации текста с сохранением контекста.
    """
    return client.chats.create(model="gemini-2.0-flash")

def generate_text_stream(chat_session, prompt: str):
    """
    Генерирует потоковый текстовый ответ от Gemini в рамках текущей сессии.
    """
    try:
        # yield text chunks to streamlit
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Произошла ошибка при обращении к Gemini: {str(e)}"
