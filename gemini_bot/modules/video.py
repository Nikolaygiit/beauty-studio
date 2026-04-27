from gradio_client import Client

def generate_video(prompt):
    """
    Генерирует видео через Gradio Space damo-vilab/modelscope-text-to-video-synthesis.
    """
    try:
        try:
            client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        except Exception as client_err:
             return None, f"Ошибка инициализации видео-клиента (Space может быть недоступен): {client_err}"

        result = client.predict(
            prompt=prompt,
            seed=-1,
            num_frames=16,
            num_inference_steps=25,
            api_name="/generate_video"
        )

        # Обычно это кортеж или словарь, Gradio может возвращать строку(путь к файлу).
        # result['video'] содержит путь к файлу mp4, если возвращается словарь в некоторых версиях API.
        # В данном space возвращается кортеж: (путь_к_видео, путь_к_gif)
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        return result, None

    except ValueError as ve:
        return None, f"Ошибка параметров генерации видео: {ve}"
    except RuntimeError as re:
        return None, f"Ошибка выполнения генерации видео: {re}"
    except Exception as e:
        return None, f"Неизвестная ошибка генерации видео: {e}"
