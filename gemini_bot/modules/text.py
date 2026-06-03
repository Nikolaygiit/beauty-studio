from google import genai
import streamlit as st

def initialize_chat_session(api_key: str):
    """
    Initializes the Gemini client and chat session.
    Stores them in Streamlit session state.
    """
    try:
        client = genai.Client(api_key=api_key)

        # Configure model to always respond in Russian
        config = genai.types.GenerateContentConfig(
            system_instruction="Всегда отвечай на русском языке.",
            temperature=0.7,
        )

        # Create a chat session
        chat = client.chats.create(
            model='gemini-2.0-flash',
            config=config
        )

        return client, chat, None
    except Exception as e:
        return None, None, f"Ошибка при инициализации Gemini: {str(e)}"

def generate_text_stream(chat_session, prompt: str):
    """
    Generates text using the Gemini chat session via streaming.
    Yields chunks of text or an error message.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n[Ошибка генерации текста: {str(e)}]"
