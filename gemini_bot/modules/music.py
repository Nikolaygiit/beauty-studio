from gradio_client import Client

def get_music_generator():
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client
    except Exception as e:
        return f"Error initializing music generator: {str(e)}"

def generate_music(client, prompt):
    if isinstance(client, str):
        return client # Error message
    try:
        result = client.predict(
            prompt=prompt,
            api_name="/generate_audio"
        )
        return result
    except Exception as e:
        return f"Error generating music: {str(e)}"
