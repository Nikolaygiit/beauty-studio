from gradio_client import Client
import logging

def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        logging.error(f"Failed to initialize music client: {e}")
        return str(e)

def generate_music(prompt: str, client) -> tuple[str | None, str | None]:
    if isinstance(client, str):
        return None, f"Music client not initialized: {client}"
    if not client:
        return None, "Music client is not available."

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Music generation error: {str(e)}"
