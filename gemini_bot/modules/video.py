import gradio_client

def get_video_client():
    return gradio_client.Client("damo-vilab/modelscope-text-to-video-synthesis")

def generate_video(client: gradio_client.Client, prompt: str) -> str:
    """
    Generates video using the gradio client and prompt.
    Returns the path to the generated video file.
    """

    # Based on the specifications: fixed parameters seed -1, 16 frames, 25 inference steps.
    result = client.predict(
        prompt,  # str  in 'Input text' Textbox component
        -1,      # float (numeric value between -1 and 2147483647) in 'Seed' Slider component
        25,      # float (numeric value between 10 and 50) in 'Number of inference steps' Slider component
        16,      # float (numeric value between 8 and 32) in 'Number of frames' Slider component
        api_name="/predict"
    )

    return result
