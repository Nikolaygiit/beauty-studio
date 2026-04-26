from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return str(e)

def generate_video(prompt):
    """Generates video using the damo-vilab/modelscope-text-to-video-synthesis space."""
    client_or_error = get_video_client()
    if isinstance(client_or_error, str):
        return None, f"Ошибка инициализации клиента генерации видео: {client_or_error}"

    client = client_or_error
    try:
        result = client.predict(
            prompt,	# str in 'text' Textbox component
            -1,	    # float (numeric value between -1 and 2147483647) in 'Seed' Slider component
            16,	    # float (numeric value between 16 and 16) in 'Max Frames' Slider component
            25,	    # float (numeric value between 10 and 50) in 'Num Inference Steps' Slider component
            api_name="/generate_video"
        )
        # The result is typically the path to the generated video file.
        # It could be a dict, string, or tuple. We'll handle common Gradio outputs.
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        elif isinstance(result, str):
            return result, None
        elif isinstance(result, dict) and 'video' in result:
             return result['video'], None
        return result, None

    except ValueError as e:
        return None, f"Ошибка значения при генерации видео: {str(e)}"
    except RuntimeError as e:
         return None, f"Ошибка выполнения при генерации видео: {str(e)}"
    except Exception as e:
        return None, f"Произошла ошибка при генерации видео: {str(e)}"
