from gradio_client import Client
import logging

def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        logging.error(f"Failed to initialize video client: {e}")
        return str(e)

def generate_video(prompt: str, client) -> tuple[str | None, str | None]:
    if isinstance(client, str):
        return None, f"Video client not initialized: {client}"
    if not client:
        return None, "Video client is not available."

    try:
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, f"Video generation error: {str(e)}"
