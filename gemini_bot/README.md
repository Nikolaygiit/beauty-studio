# Gemini Ultimate Bot

A powerful AI assistant capable of generating text, images, music, and videos using state-of-the-art models.

## Features

- **Text Generation**: Powered by Google's Gemini 1.5 Flash model. Supports chat history.
- **Image Generation**: Uses Pollinations.ai API for high-quality image generation.
- **Music Generation**: Integrates `musicgen-streaming` via Gradio Client.
- **Video Generation**: Integrates `modelscope-text-to-video-synthesis` via Gradio Client.

## Prerequisites

- Python 3.8 or higher.
- A Google Cloud API Key with access to Gemini API.

## Installation

1.  Clone the repository (if you haven't already).
2.  Navigate to the `gemini_bot` directory (or run from root).
3.  Install dependencies:

    ```bash
    pip install -r gemini_bot/requirements.txt
    ```

## Usage

1.  Run the Streamlit application:

    ```bash
    streamlit run gemini_bot/app.py
    ```

2.  Open your browser at the URL provided (usually `http://localhost:8501`).
3.  Enter your **Google API Key** in the sidebar.
4.  Select a **Mode** from the sidebar:
    - **Text/Chat**: Chat with Gemini.
    - **Image**: Generate images from text prompts.
    - **Music**: Generate music clips from text prompts.
    - **Video**: Generate short videos from text prompts.

## Notes

- **API Keys**: Your Google API Key is required for text generation. Other modalities use public Hugging Face Spaces which might have queues or rate limits.
- **Performance**: Music and Video generation can take some time depending on the load on the public Spaces.
