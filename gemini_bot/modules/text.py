from google import genai

def init_gemini(api_key):
    """
    Initializes the Gemini client and chat session.
    """
    try:
        client = genai.Client(api_key=api_key)
        chat_session = client.chats.create(model="gemini-2.0-flash")
        return client, chat_session
    except Exception as e:
        return None, None

def generate_text_stream(chat_session, prompt):
    """
    Sends a message to the Gemini chat session and streams the response.
    Catches exceptions (like blocked content) and yields the error message.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n[Ошибка Gemini API: {str(e)}]"
