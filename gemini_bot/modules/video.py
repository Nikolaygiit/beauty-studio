from gradio_client import Client

def generate_video(prompt):
    """
    Connects to the damo-vilab/modelscope-text-to-video-synthesis Gradio Space
    and generates video based on the text prompt.
    Returns a tuple: (video_path, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )

        # Depending on the API return format, it could be a tuple containing the path, or a dict.
        # We handle extracting the video path below.
        if isinstance(result, tuple) and len(result) > 0:
            video_path = result[0]
        elif isinstance(result, dict) and 'video' in result:
            video_path = result['video']
        else:
            video_path = result

        return video_path, None
    except Exception as e:
        return None, f"⚠️ Ошибка при генерации видео: {e}"
