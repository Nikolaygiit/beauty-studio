from gradio_client import Client

def generate_music(prompt: str):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio Space.
    Returns a tuple of (audio_path, error_message).
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # result is typically a tuple or string (path to wav file)
        # Assuming the first element or string itself is the filepath
        audio_path = result[0] if isinstance(result, tuple) else result
        return audio_path, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {e}"