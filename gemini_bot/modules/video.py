def generate_video(prompt, client):
    """
    Генерация видео с использованием Gradio клиента `damo-vilab/modelscope-text-to-video-synthesis`.
    """
    try:
        # Client initialization is handled in app.py to avoid recreating it
        if not client:
            return None, "Клиент не инициализирован. Пожалуйста, перезапустите приложение."

        result = client.predict(
            prompt,	# str in 'Prompt' Textbox component
            -1,	    # int | float in 'Seed' Number component (fixed)
            25,	    # int | float in 'Number of inference steps' Number component (fixed)
            16,	    # int | float in 'Number of frames' Number component (fixed)
            api_name="/generate_video"
        )
        return result, None
    except RuntimeError as e:
        return None, f"Ошибка времени выполнения на сервере генерации видео (возможно, превышен лимит): {str(e)}"
    except Exception as e:
        return None, f"Неизвестная ошибка при генерации видео: {str(e)}"
