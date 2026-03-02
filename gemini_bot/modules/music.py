def generate_music(client, prompt: str, audio_length: float = 15.0, play_steps: float = 1.5, seed: float = 5):
    """
    Generates music using the provided Gradio client (sanchit-gandhi/musicgen-streaming).

    Args:
        client: The Gradio Client instance.
        prompt: Text prompt for music generation.
        audio_length: Length of generated audio in seconds.
        play_steps: Play steps in seconds.
        seed: Random seed.

    Returns:
        The path to the generated audio file.
    """
    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=audio_length,
            play_steps_in_s=play_steps,
            seed=seed,
            fn_index=0
        )
        return result
    except Exception as e:
        raise Exception(f"Failed to generate music: {str(e)}")
