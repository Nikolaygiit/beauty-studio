from gradio_client import Client
import os

def generate_music(prompt, duration=10, hf_token=None):
    """
    Generates music using facebook/MusicGen Space.

    Args:
        prompt (str): Description of the music.
        duration (int): Duration in seconds.
        hf_token (str): Optional Hugging Face token.

    Returns:
        str: Path to the generated audio file, or None on failure.
    """
    try:
        # Check if HF_TOKEN is in environment if not provided
        if not hf_token:
            hf_token = os.getenv("HF_TOKEN")

        client = Client("facebook/MusicGen", hf_token=hf_token)
        result = client.predict(
            prompt,
            None, # File (audio) for melody conditioning
            duration, # Duration (seconds)
            api_name="/predict"
        )
        return result
    except Exception as e:
        print(f"Error generating music: {e}")
        return None
