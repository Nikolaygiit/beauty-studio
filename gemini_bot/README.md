# Gemini Ultimate Bot 🤖

The **Gemini Ultimate Bot** is an all-in-one AI assistant built with Streamlit. It integrates powerful AI models to generate text, images, music, and videos.

## Features

- **💬 Chat**: Conversational AI powered by **Google Gemini 1.5 Flash**. Supports text and image inputs (multimodal).
- **🖼️ Image Generation**: Create images from text prompts using **Pollinations.ai** (Free, no API key required).
- **🎵 Music Generation**: Generate short music clips using **MusicGen** via Hugging Face Spaces.
- **🎥 Video Generation**: Generate short videos from text using **ModelScope Text-to-Video** via Hugging Face Spaces.

## Prerequisites

- Python 3.8+
- [Google API Key](https://aistudio.google.com/app/apikey) (for Chat)
- [Hugging Face Token](https://huggingface.co/settings/tokens) (Optional, but recommended for Music/Video to avoid queues/errors)

## Installation

1.  **Navigate to the bot directory:**
    ```bash
    cd gemini_bot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables:**
    - Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env
        ```
    - Open `.env` and add your keys:
        ```
        GOOGLE_API_KEY=your_key_here
        HF_TOKEN=your_token_here
        ```
    - *Alternatively, you can enter these keys directly in the sidebar of the application.*

## Running the Bot

Run the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your default web browser (usually at `http://localhost:8501`).

## Troubleshooting

- **Music/Video Error**: "The current space is in the invalid state" or "Queue is full".
    - These features rely on public Hugging Face Spaces which can be busy.
    - Try adding a **Hugging Face Token** in the sidebar settings.
    - If the specific Space is down, you may need to wait or update the code to point to a new Space URL.

## License

MIT
