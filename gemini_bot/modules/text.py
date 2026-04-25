from google import genai

def init_chat_session(api_key):
    """Initializes the Gemini chat session with google-genai."""
    try:
        client = genai.Client(api_key=api_key)
        chat_session = client.chats.create(model="gemini-2.0-flash")
        return client, chat_session, None
    except Exception as e:
        return None, None, f"Error initializing Gemini client: {e}"

def generate_text_stream(chat_session, prompt):
    """Generates a text stream response using Gemini API."""
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\\n\\n*Error during generation: {e}*"