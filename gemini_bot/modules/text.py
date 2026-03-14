from google import genai

def get_text_response(api_key: str, prompt: str, chat_session):
    """
    Generate text using Gemini 2.5 Flash model with conversation history.
    Streams the output if possible, otherwise returns the full response.
    """
    if not api_key:
        yield "Ошибка: Пожалуйста, введите ваш Google API Key в боковой панели."
        return

    try:
        if chat_session is None:
            # This shouldn't happen if app.py initializes it, but just in case
            client = genai.Client(api_key=api_key)
            chat_session = client.chats.create(model="gemini-2.5-flash")

        # Use streaming for better user experience
        response_stream = chat_session.send_message_stream(prompt)

        for chunk in response_stream:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"Произошла ошибка при генерации текста: {str(e)}"

def init_chat_session(api_key: str):
    """Initializes and returns a new chat session."""
    if not api_key:
        return None
    try:
        client = genai.Client(api_key=api_key)
        return client.chats.create(model="gemini-2.5-flash")
    except Exception as e:
        print(f"Error initializing chat session: {e}")
        return None
