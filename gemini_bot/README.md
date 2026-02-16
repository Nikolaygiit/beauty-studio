# Gemini Ultimate Bot 🤖

A comprehensive AI Assistant powered by Google's Gemini models and various generative AI tools. This application provides a unified interface for Text, Image, Music, and Video generation.

## Features ✨

- **💬 Smart Chat**: Powered by **Gemini 1.5 Flash**. Supports text and image inputs (multimodal).
- **🖼️ Image Generation**: High-quality image generation powered by **Pollinations.ai** (Flux/Stable Diffusion).
- **🎵 Music Generation**: Text-to-Music capabilities using **Facebook MusicGen** (via HuggingFace Spaces).
- **🎥 Video Generation**: Text-to-Video capabilities using **ModelScope** (via HuggingFace Spaces).

## Prerequisites 🛠️

- **Python 3.8+**
- **Google API Key**: Required for Chat. Get it for free at [Google AI Studio](https://aistudio.google.com/).
- **HuggingFace Token** (Optional): Recommended for faster Music/Video generation. Get it at [HuggingFace Settings](https://huggingface.co/settings/tokens).

## Installation 📥

1.  **Clone or Download** this repository.
2.  **Navigate** to the `gemini_bot` directory:
    ```bash
    cd gemini_bot
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage 🚀

1.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```
2.  **Open in Browser**: The app should automatically open in your default browser (usually at `http://localhost:8501`).
3.  **Configure**:
    - Enter your **Google API Key** in the sidebar.
    - (Optional) Enter your **HuggingFace Token** for better performance on media generation.

## Capabilities Guide 📚

### Chat 💬
- Type your message in the chat input at the bottom.
- **Upload an Image**: Expand the "Upload Image for Analysis" section to chat about an image.
- Gemini maintains context of the conversation.

### Image Generation 🖼️
- Go to the **Generate Image** tab.
- Describe the image you want (e.g., "A futuristic city in the style of cyberpunk").
- Click **Generate**.
- You can download the result.

### Music Generation 🎵
- Go to the **Generate Music** tab.
- Describe the music (e.g., "Lo-fi hip hop beat").
- Set the duration (longer takes more time).
- Click **Generate**.
- *Note: This uses external APIs and may have a queue.*

### Video Generation 🎥
- Go to the **Generate Video** tab.
- Describe the scene (e.g., "A panda eating bamboo").
- Click **Generate**.
- *Note: Video generation is resource-intensive and may take several minutes.*

## Troubleshooting 🔧

- **"API Key not found"**: Ensure you entered the key in the sidebar or set it in a `.env` file.
- **"Module not found"**: Make sure you installed requirements and are running `streamlit run app.py` from inside the `gemini_bot` folder.
- **Media Generation Fails**:
    - The external services (HuggingFace Spaces) might be busy or overloaded.
    - Try again later or use a HuggingFace Token.
    - Check your internet connection.

## License 📄
MIT License
