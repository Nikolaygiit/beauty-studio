import streamlit as st
import urllib.parse

def generate_image_url(prompt):
    """Generates an image URL using Pollinations.ai."""
    encoded_prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}"

def handle_image_generation():
    """Handles the UI and logic for image generation."""
    st.header("Image Generation")
    prompt = st.text_input("Enter a prompt for the image:", "A futuristic city with flying cars")

    if st.button("Generate Image"):
        if prompt:
            with st.spinner("Generating image..."):
                image_url = generate_image_url(prompt)
                st.image(image_url, caption=prompt)
        else:
            st.warning("Please enter a prompt.")
