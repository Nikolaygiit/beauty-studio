import gradio_client

def get_music_client():
    return gradio_client.Client("sanchit-gandhi/musicgen-streaming")

def generate_music(client: gradio_client.Client, prompt: str) -> str:
    """
    Generates music using the gradio client and prompt.
    Returns the path to the generated audio file.
    """

    # Generate the music using the Gradio client
    result = client.predict(
        text_prompt=prompt,
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=5,
        api_name="/generate_audio"
    )

    return result
