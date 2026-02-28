def generate_music(client, prompt):
    try:
        result = client.predict(
            text=prompt,
            melody=None,
            fn_index=0
        )
        # The result returns a tuple where the first element is the path to the generated audio
        return result[0]
    except Exception as e:
        return f"An error occurred: {e}"
