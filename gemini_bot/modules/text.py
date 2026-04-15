from google import genai

def get_gemini_client(api_key: str):
    """
    Initializes and returns the Google GenAI client.
    """
    return genai.Client(api_key=api_key)

def init_chat_session(client, chat_history=None):
    """
    Initializes a new chat session with the given history.
    """
    if chat_history is None:
        chat_history = []
    return client.chats.create(model="gemini-2.0-flash")

def generate_text_stream(chat_session, prompt: str):
    """
    Generates a text response stream using the current chat session.
    """
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Ошибка при генерации текста:** {str(e)}"
