from google import genai
import traceback

def get_gemini_client(api_key: str):
    """
    Initializes and returns the Gemini client using the given API key.
    Returns a tuple of (client, error_message).
    """
    if not api_key:
        return None, "API key is required"
    try:
        client = genai.Client(api_key=api_key)
        # Attempt to create a chat to test the connection and model
        chat = client.chats.create(
            model="gemini-2.0-flash",
            config={
                "system_instruction": "You are a helpful and intelligent assistant. Always reply in Russian."
            }
        )
        return client, None
    except Exception as e:
        error_msg = f"Failed to initialize Gemini client: {e}"
        print(f"Error: {error_msg}")
        traceback.print_exc()
        return None, error_msg

def initialize_chat_session(client):
    """
    Initializes a chat session using the given Gemini client.
    """
    if not client:
        return None
    try:
        chat = client.chats.create(
            model="gemini-2.0-flash",
            config={
                "system_instruction": "You are a helpful and intelligent assistant. Always reply in Russian."
            }
        )
        return chat
    except Exception as e:
        print(f"Failed to create chat session: {e}")
        return None
