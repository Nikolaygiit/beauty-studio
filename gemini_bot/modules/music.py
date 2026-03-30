from gradio_client import Client

def generate_music(prompt, client):
    try:
        result = client.predict(
            prompt,
            api_name="/generate_audio"
        )
        # `result` is typically the path to the generated audio file
        return result
    except Exception as e:
        return f"Error generating music: {e}"

def init_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Error initializing music client: {e}"
