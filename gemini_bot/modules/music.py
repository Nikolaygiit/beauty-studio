from gradio_client import Client

def init_music_client():
    """Initializes the music generator client.
    Handles RUNTIME_ERROR from the gradio space if it occurs.
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client
    except Exception as e:
        error_msg = str(e)
        if "RUNTIME_ERROR" in error_msg:
            return f"Ошибка: Музыкальный сервер сейчас недоступен (RUNTIME_ERROR)."
        return f"Ошибка инициализации музыки: {error_msg}"

def generate_music(client, prompt: str, length_s: float = 15.0, seed: float = 5.0):
    """Generates music using the provided music generator client."""
    if isinstance(client, str):
        # Client initialization failed, return the error message
        return client, None

    try:
        # Default streaming play_steps_in_s is 1.5
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=length_s,
            play_steps_in_s=1.5,
            seed=seed,
            api_name="/generate_audio"
        )

        # result is a filepath to the generated audio
        return None, result

    except Exception as e:
        return f"Произошла ошибка при генерации музыки: {str(e)}", None
