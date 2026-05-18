from gradio_client import Client

def get_music_client():
    """Initializes the music client."""
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации MusicGen клиента: {str(e)}"

def generate_music(client: Client, prompt: str):
    """
    Generates music using the provided Gradio client.
    Returns (media_path, error_msg).
    """
    if not client:
        return None, "Клиент MusicGen не инициализирован."

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
