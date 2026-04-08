import streamlit as st
from google import genai
from google.genai import errors

def get_gemini_client(api_key):
    """Initializes and returns the Gemini client."""
    return genai.Client(api_key=api_key)

def get_chat_session(client):
    """Initializes and returns a new chat session."""
    return client.chats.create(model="gemini-2.0-flash")

def generate_text_stream(chat_session, prompt):
    """
    Generates text response using Gemini client.
    Handles streaming and exceptions like API errors.
    """
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except errors.APIError as e:
        yield f"API Error: {e}"
    except Exception as e:
        yield f"An error occurred: {e}"
