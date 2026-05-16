from gradio_client import Client

def generate_video(prompt):
    """
    Generates a video using the damo-vilab/modelscope-text-to-video-synthesis space.
    Returns a tuple of (video_path, error_message).
    """
    if not prompt:
        return None, "Prompt is missing."

    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        # The result from generate_video is a path to the video file or a dictionary containing the path
        if isinstance(result, dict) and 'video' in result:
            return result['video'], None
        return result, None
    except Exception as e:
        return None, f"Failed to generate video: {str(e)}"
