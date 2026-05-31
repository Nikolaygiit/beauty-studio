from google import genai

def get_text_client(api_key: str):
    return genai.Client(api_key=api_key)

def start_chat_session(client):
    return client.chats.create(
        model="gemini-2.0-flash",
        config={
            "system_instruction": "Ты должен всегда отвечать на русском языке."
        }
    )

def stream_text_response(chat_session, prompt: str):
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n[Ошибка при генерации текста: {str(e)}]"
