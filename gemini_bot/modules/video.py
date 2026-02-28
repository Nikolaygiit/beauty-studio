def generate_video(client, prompt):
    try:
        result = client.predict(
            prompt,	# str in 'Input prompt' Textbox component
            -1,	    # int | float (numeric value between -1 and 2147483647) in 'Seed' Slider component
            16,	    # int | float (numeric value between 16 and 16) in 'Number of Frames' Slider component
            25,	    # int | float (numeric value between 10 and 50) in 'Number of Inference Steps' Slider component
            fn_index=0
        )
        # The result returns a dictionary where 'video' is a path to the generated video
        if 'video' in result:
             return result['video']
        return result
    except Exception as e:
        return f"An error occurred: {e}"
