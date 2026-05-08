from gradio_client import Client

def generate_music(prompt):
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # result is typically a path to the generated audio file
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
