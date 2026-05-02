from google import genai
import streamlit as st

def init_client(api_key: str) -> genai.Client:
    """Initialize the Google GenAI client."""
    return genai.Client(api_key=api_key)

def init_chat_session(client: genai.Client):
    """Initialize a chat session using the gemini-2.0-flash model."""
    # We use gemini-2.0-flash for standard conversational text
    return client.chats.create(model="gemini-2.0-flash")

def stream_text_response(chat_session, prompt: str):
    """Generate a streaming text response from the model."""
    try:
        # Provide the generator to be consumed by st.write_stream or similar
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            yield chunk.text
    except Exception as e:
        yield f"\n\n**Error during text generation:** {str(e)}"
