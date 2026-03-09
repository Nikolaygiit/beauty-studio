from gradio_client import Client

def init_generator():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка инициализации генератора музыки: {e}"

def generate_music(client, prompt, duration=10):
    if isinstance(client, str): # Error during init
        return client

    try:
        result = client.predict(
            prompt,	# str in 'Describe your music' Textbox component
            duration, # float (numeric value between 1 and 30)
            api_name="/generate_audio"
        )
        return result
    except Exception as e:
        return f"Ошибка при генерации музыки: {e}"