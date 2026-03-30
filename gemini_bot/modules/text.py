from google import genai

def initialize_chat(api_key):
    try:
        client = genai.Client(api_key=api_key)
        chat = client.chats.create(model="gemini-2.0-flash")
        return chat
    except Exception as e:
        return f"Error initializing chat: {e}"

def generate_text_stream(chat_session, prompt):
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n[Error during text generation: {e}]"
