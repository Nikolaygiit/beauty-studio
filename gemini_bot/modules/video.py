def generate_video(client, prompt: str):
    """
    Generates video using the provided Gradio client (damo-vilab/modelscope-text-to-video-synthesis).

    Uses fixed parameters:
    - seed: -1 (random)
    - num_frames: 16
    - num_inference_steps: 25

    Args:
        client: The Gradio Client instance.
        prompt: Text prompt for video generation.

    Returns:
        The path to the generated video file.
    """
    try:
        # NOTE: If this space is down, this call will fail.
        # Ensure error handling on the calling side.
        result = client.predict(
            prompt,	    # str  in 'Prompt' Textbox component
            -1,	        # float (numeric value between -1 and 2147483647) in 'Seed' Slider component
            16,	        # float (numeric value between 16 and 16) in 'Number of Frames' Slider component
            25,	        # float (numeric value between 10 and 50) in 'Number of Inference Steps' Slider component
            api_name="/video"
        )
        return result
    except Exception as e:
        raise Exception(f"Failed to generate video: {str(e)}")
