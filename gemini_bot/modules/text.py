from google import genai

def get_chat_session(api_key):
    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model="gemini-2.0-flash")
    return chat

def generate_text_stream(chat_session, prompt):
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Error generating text: {str(e)}"
