import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_video_client():
    return Client("damo-vilab/modelscope-text-to-video-synthesis")

def generate_video(prompt):
    try:
        # Connect to the Hugging Face Space for video generation
        client = get_video_client()

        # Call the generate_video endpoint using the fixed positional parameters
        # (prompt, seed, num_frames, num_inference_steps)
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )

        # In Gradio v3/v4 outputs, typically the result could be a file path, string or dictionary.
        # Assuming the first element (or result directly) is the path based on typical behavior.
        # Often it returns a dictionary with 'video' or directly the filepath.
        # Here we just pass the result to the caller to handle/display it.
        return result, None
    except ValueError as ve:
        return None, f"Ошибка параметров при генерации видео: {ve}"
    except RuntimeError as re:
        return None, f"Ошибка выполнения при генерации видео: {re}"
    except Exception as e:
        return None, f"Неизвестная ошибка при генерации видео: {e}"
