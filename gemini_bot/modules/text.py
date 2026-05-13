from google import genai
import streamlit as st

def initialize_chat(api_key):
    """Initializes and returns a Gemini client and chat session."""
    try:
        client = genai.Client(api_key=api_key)
        # Using gemini-2.0-flash as per memory
        chat = client.chats.create(model="gemini-2.0-flash")
        return client, chat
    except Exception as e:
        return None, f"Failed to initialize Gemini client: {e}"

def generate_text_stream(chat_session, prompt):
    """Generates a streaming text response from the Gemini model."""
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\nAn error occurred during text generation: {e}"
