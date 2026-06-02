from google import genai

def get_gemini_client(api_key: str):
    """Initializes and returns the Gemini client."""
    return genai.Client(api_key=api_key)

def init_chat_session(client):
    """Initializes a new chat session with system instructions."""
    config = genai.types.GenerateContentConfig(
        system_instruction="Ты — полезный ИИ-ассистент. Отвечай всегда на русском языке."
    )
    return client.chats.create(
        model="gemini-2.0-flash",
        config=config
    )

def generate_text_stream(chat_session, prompt: str):
    """
    Generates text from a prompt using the existing chat session to keep history.
    Yields text chunks.
    """
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Ошибка при генерации текста:** {str(e)}"
