from gradio_client import Client

def get_video_client():
    """Initializes and returns the Gradio client for video generation."""
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client
    except Exception as e:
        return f"Ошибка инициализации видео модуля: {e}"

def generate_video(client, prompt):
    """Generates video based on the prompt using the Gradio client."""
    if isinstance(client, str): # Error during initialization
        return client, None

    try:
        # Based on typical usage for this space
        result = client.predict(
            prompt=prompt,
            seed=-1,
            num_frames=16,
            num_inference_steps=25,
            api_name="/predict"
        )
        # result is typically a path/URL to the video or a dict containing it
        video_path = result.get("video") if isinstance(result, dict) else result
        return None, video_path
    except Exception as e:
        return f"Произошла ошибка при генерации видео: {e}", None
