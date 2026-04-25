from gradio_client import Client

def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return None

def generate_video(client, prompt):
    """Generates video using modelscope text-to-video space."""
    if not client:
        return None, "Video generation client is not initialized."
    try:
        # fixed positional parameters: prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        if isinstance(result, tuple) and len(result) > 0:
             # The result usually contains a path to the generated video
             return result[0], None
        elif isinstance(result, dict) and "video" in result:
             return result["video"], None
        return result, None
    except ValueError as e:
         return None, f"ValueError generating video: {e}"
    except RuntimeError as e:
         return None, f"RuntimeError generating video: {e}"
    except Exception as e:
        return None, f"Error generating video: {e}"