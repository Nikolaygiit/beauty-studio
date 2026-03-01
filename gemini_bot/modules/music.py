import time
from gradio_client import Client

def get_music_client():
    """Initializes and returns the Gradio client for music generation."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        print(f"Failed to initialize music client: {e}")
        return None

def generate_music(prompt: str, client: Client):
    """
    Generates music using Gradio client for sanchit-gandhi/musicgen-streaming
    """
    if client is None:
        return "Error: Music client is not initialized."

    try:
        result = client.predict(
            prompt,	# str in 'Describe your music' Textbox component
            fn_index=0
        )
        return result
    except Exception as e:
        return f"Error generating music: {str(e)}"
