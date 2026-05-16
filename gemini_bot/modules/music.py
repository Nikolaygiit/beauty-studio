from gradio_client import Client

def generate_music(prompt):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming space.
    Returns a tuple of (audio_path, error_message).
    """
    if not prompt:
        return None, "Prompt is missing."

    try:
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
        return None, f"Failed to generate music: {str(e)}"
