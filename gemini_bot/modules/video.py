from gradio_client import Client

def generate_video(client, prompt):
    try:
        # Note: According to memory, the API expects positional parameters
        # prompt, -1 (seed), 16 (num_frames), 25 (num_inference_steps)
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        if isinstance(result, tuple):
             return result[0], None
        return result, None
    except Exception as e:
        return None, str(e)
