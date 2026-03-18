import logging
from google import genai

logging.basicConfig(level=logging.INFO)

def init_chat_session(api_key):
    """Initializes the chat session with the Gemini API."""
    try:
        client = genai.Client(api_key=api_key)
        chat = client.chats.create(model="gemini-2.0-flash")
        return chat
    except Exception as e:
        logging.error(f"Error initializing chat session: {e}")
        return None

def generate_text_stream(chat, prompt):
    """Generates text from the Gemini API and yields it as a stream."""
    try:
        response_stream = chat.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        error_msg = f"\n[Ошибка генерации текста: {str(e)}]"
        logging.error(error_msg)
        yield error_msg
