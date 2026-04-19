import logging
from gradio_client import Client

def generate_music(prompt, client=None):
    """
    Generates music using sanchit-gandhi/musicgen-streaming space.
    Requires a pre-initialized client to avoid recreating it per request.
    Returns (audio_path, None) on success, or (None, error_message) on failure.
    """
    try:
        if client is None:
            # Fallback if no client passed, though app.py should handle it
            client = Client("sanchit-gandhi/musicgen-streaming")

        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Music Generation Error: {error_msg}")
        return None, f"Ошибка при генерации музыки: {error_msg}"
