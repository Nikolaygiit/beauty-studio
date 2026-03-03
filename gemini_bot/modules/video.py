import os
from gradio_client import Client

def get_video_client():
    """Initializes and returns the Gradio client for the video generation model."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return None

def generate_video(client, prompt):
    """
    Generates video based on the prompt using the initialized client.
    Uses fixed parameters: seed -1, 16 frames, and 25 inference steps.
    Returns the path to the downloaded video file or an error message.
    """
    if client is None:
        return None, "Video generation client could not be initialized."

    try:
        # According to standard modelscope API:
        # prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt=prompt,
            seed=-1,
            num_frames=16,
            num_inference_steps=25,
            api_name="/generate"
        )

        # Result is typically a tuple or dict containing the file path
        if isinstance(result, tuple):
            video_path = result[0]
        elif isinstance(result, dict) and "video" in result:
            video_path = result["video"]
        elif isinstance(result, str):
            video_path = result
        else:
            return None, f"Неизвестный формат ответа: {result}"

        return video_path, None
    except Exception as e:
        return None, f"Ошибка генерации видео: {str(e)}"
