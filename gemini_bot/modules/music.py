from gradio_client import Client

def generate_music(prompt: str, client: Client) -> str:
    """
    Generates music using the provided gradio client connected to 'sanchit-gandhi/musicgen-streaming'.
    """
    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # The result returns a tuple, usually the path to the generated audio file is the first or second element.
        # Based on the musicgen-streaming space, it typically returns a tuple of (audio_path, video_path)
        # Wait, the prompt says "returns a tuple", let's return result to be safe or index 0 if it's a tuple.
        if isinstance(result, tuple) and len(result) > 0:
            return result[0]
        return result
    except Exception as e:
        return f"Ошибка при генерации музыки: {str(e)}"
