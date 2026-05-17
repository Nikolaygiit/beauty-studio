from gradio_client import Client

def generate_music(client, prompt):
    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # result is typically a tuple or string (path to audio file)
        # Gradio client usually returns the path to the downloaded file
        if isinstance(result, tuple):
             return result[0], None
        return result, None
    except Exception as e:
        return None, str(e)
