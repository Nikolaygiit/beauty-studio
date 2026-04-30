from google import genai

def get_gemini_client(api_key: str):
    """
    Initializes and returns the Gemini client.
    """
    return genai.Client(api_key=api_key)

def start_chat_session(client):
    """
    Starts a chat session with the gemini-2.0-flash model.
    """
    return client.chats.create(model="gemini-2.0-flash")
