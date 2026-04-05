from gradio_client import Client

def get_music_client():
    """Initializes and returns the Gradio client for music generation."""
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client
    except Exception as e:
        return f"Ошибка инициализации музыкального модуля: {e}"

def generate_music(client, prompt):
    """Generates music based on the prompt using the Gradio client."""
    if isinstance(client, str): # Error during initialization
        return client, None

    try:
        result = client.predict(
            prompt=prompt,
            api_name="/generate_audio"
        )
        # result is typically the path to the generated audio file
        return None, result
    except Exception as e:
        return f"Произошла ошибка при генерации музыки: {e}", None
