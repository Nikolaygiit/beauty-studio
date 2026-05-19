from google import genai

def init_chat_session(api_key):
    try:
        client = genai.Client(api_key=api_key)
        # Using the specified gemini-2.0-flash model and ensuring Russian response
        config = genai.types.GenerateContentConfig(
            system_instruction="Всегда отвечай на русском языке."
        )
        # Initialize a new chat session using the core client
        chat = client.chats.create(model="gemini-2.0-flash", config=config)
        return client, chat, None
    except Exception as e:
        return None, None, f"Ошибка инициализации Gemini: {e}"

def generate_text_stream(chat, prompt):
    try:
        response_stream = chat.send_message_stream(prompt)
        return response_stream, None
    except Exception as e:
        return None, f"Ошибка при генерации текста: {e}"
