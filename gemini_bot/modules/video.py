from gradio_client import Client

def init_generator():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации генератора видео: {e}"

def generate_video(client, prompt):
    if isinstance(client, str): # Error during init
        return client

    try:
        result = client.predict(
            prompt, # str in 'Prompt' Textbox component
            -1, # int (numeric value between -1 and 2147483647) in 'Seed' Slider component
            16, # int (numeric value between 16 and 32) in 'Number of Frames' Slider component
            25, # int (numeric value between 10 and 50) in 'Number of Inference Steps' Slider component
            api_name="/generate_video"
        )
        # result typically returns a path or dict containing a path
        if isinstance(result, dict) and 'video' in result:
            return result['video']
        return result
    except Exception as e:
        return f"Ошибка при генерации видео: {e}"