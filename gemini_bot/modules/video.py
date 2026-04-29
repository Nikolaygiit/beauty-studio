from gradio_client import Client

def generate_video(prompt):
    """
    Генерирует видео, используя Gradio Client и damo-vilab/modelscope-text-to-video-synthesis.
    Возвращает кортеж (video_path, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        result = client.predict(
            prompt,
            -1, # seed
            16, # num_frames
            25, # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except ValueError as ve:
        return None, f"Ошибка значений при генерации видео: {ve}"
    except RuntimeError as re:
        return None, f"Ошибка выполнения при генерации видео: {re}"
    except Exception as e:
        return None, f"Неизвестная ошибка при генерации видео: {e}"
