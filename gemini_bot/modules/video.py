from gradio_client import Client

def generate_video(prompt):
    """
    Generates a video using the damo-vilab/modelscope-text-to-video-synthesis space.
    Returns a tuple (video_path, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        result = client.predict(
            prompt,  # prompt
            -1,      # seed
            16,      # num_frames
            25,      # num_inference_steps
            api_name="/generate_video"
        )

        # Extract path. Note result might be structured differently based on API changes,
        # but usually returns the path to the video or a dictionary containing the path.
        video_path = result['video'] if isinstance(result, dict) and 'video' in result else result
        return video_path, None
    except ValueError as e:
        return None, f"Ошибка в значениях для видео (возможно сервер перегружен): {str(e)}"
    except RuntimeError as e:
        return None, f"Ошибка выполнения при генерации видео: {str(e)}"
    except Exception as e:
        return None, f"Неизвестная ошибка генерации видео: {str(e)}"
