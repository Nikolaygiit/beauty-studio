from gradio_client import Client
import os

def generate_music(prompt):
    """
    Generates music using the Facebook MusicGen Small model via Hugging Face Spaces.
    Args:
        prompt (str): Description of the music.
    Returns:
        str: Path to the generated audio file.
    """
    try:
        # loading the client might take a moment
        client = Client("facebook/musicgen-small")

        # The predict parameters depend on the specific space's implementation.
        # For musicgen-small: text, melody (optional)
        result = client.predict(
            prompt, # str  in 'Describe your music' Textbox component
            None,   # str (filepath or URL to file) in 'File' Audio component
            api_name="/predict"
        )

        # Result is typically the path to the audio file
        return result
    except Exception as e:
        print(f"Error generating music: {e}")
        # Fallback or returning None
        return None
