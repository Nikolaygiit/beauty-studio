from gradio_client import Client

def initialize_music_client():
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client
    except Exception as e:
        return f"Ошибка при инициализации клиента музыки: {str(e)}"

def generate_music(client, prompt):
    if isinstance(client, str):
        return None, client # Return error message

    try:
        result = client.predict(
            prompt=prompt,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
