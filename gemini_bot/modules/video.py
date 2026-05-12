import os
from gradio_client import Client

def generate_video(prompt):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio space.
    Returns (video_path, None) on success, or (None, error_message) on failure.
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

        # The result typically contains a path or dictionary with the path
        if isinstance(result, dict) and "video" in result:
            video_path = result["video"]
        elif isinstance(result, tuple) or isinstance(result, list):
            video_path = result[0]
        else:
            video_path = result

        if video_path and os.path.exists(video_path):
            return video_path, None
        else:
            return None, "Видеофайл не был сгенерирован или не найден."
    except ValueError as e:
         return None, f"Ошибка значения при генерации видео: {e}"
    except RuntimeError as e:
         return None, f"Ошибка выполнения при генерации видео: {e}"
    except Exception as e:
        return None, f"Неизвестная ошибка при генерации видео: {e}"
