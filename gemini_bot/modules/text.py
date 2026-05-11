import os
from google import genai
from google.genai import types

def init_client(api_key):
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, str(e)

def start_chat(client):
    try:
        chat = client.chats.create(model="gemini-2.0-flash")
        return chat, None
    except Exception as e:
        return None, str(e)

def generate_text_stream(chat, prompt):
    try:
        response = chat.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Error:** {str(e)}"
