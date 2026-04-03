from gradio_client import Client

def get_music_client():
    """Initializes the music generation client."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Error initializing music client: {e}"

def generate_music(client, prompt):
    """Generates music based on the prompt."""
    try:
        result = client.predict(
            text=prompt,
            melody=None,
            api_name="/generate_audio"
        )
        # The result typically contains a path to the generated audio file
        return result
    except Exception as e:
        return f"Error generating music: {e}"
