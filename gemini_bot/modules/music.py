from gradio_client import Client

def generate_music(prompt):
    """
    Connects to the sanchit-gandhi/musicgen-streaming Gradio Space
    and generates audio based on the text prompt.
    Returns a tuple: (audio_path, error_message).
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
        # `result` is typically a tuple of (audio_file_path, something_else) or just the audio file path
        # depending on the endpoint. We attempt to extract the file path.
        if isinstance(result, tuple) and len(result) > 0:
            audio_path = result[0]
        else:
            audio_path = result

        return audio_path, None
    except Exception as e:
        return None, f"⚠️ Ошибка при генерации музыки: {e}"
