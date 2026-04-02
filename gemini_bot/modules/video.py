from gradio_client import Client

def generate_video(prompt):
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        result = client.predict(
            prompt=prompt,
            api_name="/predict"
        )
        return result
    except Exception as e:
        return f"Ошибка генерации видео: {e}"
