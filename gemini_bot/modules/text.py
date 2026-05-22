from google import genai
import streamlit as st

def initialize_chat(client: genai.Client):
    """Initializes the chat session using the genai client."""
    return client.chats.create(
        model="gemini-2.0-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction="Ты — полезный ИИ-помощник. Всегда отвечай на русском языке.",
            temperature=0.7,
        )
    )

def generate_text_stream(chat_session, prompt: str):
    """Yields chunks of text from the streaming response."""
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Ошибка при генерации текста:** {str(e)}"
