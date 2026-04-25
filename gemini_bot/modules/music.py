from gradio_client import Client

def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return None

def generate_music(client, prompt):
    """Generates music using musicgen-streaming space."""
    if not client:
        return None, "Music generation client is not initialized."
    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # result is typically a tuple or string path depending on the gradio endpoint setup
        # For musicgen-streaming, predict might return a file path.
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        return result, None
    except Exception as e:
        return None, f"Error generating music: {e}"