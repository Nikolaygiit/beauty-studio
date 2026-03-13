# Gemini Ultimate Bot

A Streamlit application that uses various AI models to generate text, images, music, and videos based on user prompts.

## Features

* **Text Generation:** Uses Google's Gemini (`gemini-2.5-flash`) for conversational text generation.
* **Image Generation:** Uses the Pollinations.ai API to create images from text prompts.
* **Music Generation:** Uses the `sanchit-gandhi/musicgen-streaming` Hugging Face Space via `gradio_client`.
* **Video Generation:** Uses the `damo-vilab/modelscope-text-to-video-synthesis` Hugging Face Space via `gradio_client`.

## Setup

1. Install dependencies:
   ```bash
   pip install -r gemini_bot/requirements.txt
   ```

2. Run the application:
   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)/gemini_bot && streamlit run gemini_bot/app.py
   ```

## Usage

1. Enter your `GOOGLE_API_KEY` in the sidebar to enable text generation.
2. Type a message in the chat input.
3. Use specific keywords to trigger different generation types:
   * **Images:** Start your prompt with "нарисуй", "фото", or "изображение".
   * **Music:** Include "музыка" or "песня" in your prompt.
   * **Video:** Include "видео" or "ролик" in your prompt.
   * **Text:** Any other prompt will be sent to Gemini.
