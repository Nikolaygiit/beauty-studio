from gradio_client import Client

def generate_music(prompt):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming space.
    Returns a tuple (audio_path, error_message).
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
        # The result might be a tuple where the first element is the path to the audio file
        audio_path = result[0] if isinstance(result, tuple) else result
        return audio_path, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
