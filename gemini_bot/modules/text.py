from google import genai

def get_gemini_client(api_key):
    """Initializes and returns a Gemini client."""
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации Gemini: {e}"

def create_chat_session(client, model_name="gemini-2.0-flash"):
    """Creates a chat session using the provided Gemini client."""
    try:
        chat = client.chats.create(model=model_name)
        return chat, None
    except Exception as e:
        return None, f"Ошибка создания чата: {e}"

def generate_text_stream(chat_session, prompt):
    """Generates a text response stream from the chat session."""
    try:
        response = chat_session.send_message_stream(prompt)
        return response, None
    except Exception as e:
        return None, f"Ошибка генерации текста: {e}"
