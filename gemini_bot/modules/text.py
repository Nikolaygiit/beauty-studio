from google import genai
from google.genai import types
from typing import Tuple, Optional, Any

def get_gemini_client(api_key: str) -> Tuple[Optional[genai.Client], Optional[str]]:
    """
    Initializes and returns the Gemini client and error message tuple.
    """
    try:
        if not api_key:
            return None, "API key is required."
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, str(e)

def get_chat_session(client: genai.Client) -> Any:
    """
    Initializes a chat session with the gemini-2.0-flash model,
    configured to respond in Russian.
    """
    return client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="Всегда отвечай на русском языке.",
            temperature=0.7,
        )
    )

def generate_text_stream(chat_session, prompt: str):
    """
    Generates text via streaming and yields the chunks.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Произошла ошибка при генерации текста: {str(e)}"
