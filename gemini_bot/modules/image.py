
class ImageGenerator:
    def generate_image(self, prompt):
        """
        Generates an image URL using Pollinations.ai API.
        """
        # Encode prompt for URL
        prompt_encoded = prompt.replace(" ", "%20")
        url = f"https://image.pollinations.ai/prompt/{prompt_encoded}"
        return url
