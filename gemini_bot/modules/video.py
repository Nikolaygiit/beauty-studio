from gradio_client import Client

def generate_video(prompt: str):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio Space.
    Returns a tuple of (video_path, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        result = client.predict(
            prompt,  # text prompt
            -1,      # seed
            16,      # num_frames
            25,      # num_inference_steps
            api_name="/generate_video"
        )

        # result is typically a path to an mp4 file or a dictionary
        if isinstance(result, dict) and 'video' in result:
             video_path = result['video']
        else:
             video_path = result

        return video_path, None
    except Exception as e:
        return None, f"Ошибка при генерации видео (возможно, сервер перегружен): {e}"