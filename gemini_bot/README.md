# Gemini Ultimate Bot

This is a comprehensive, multi-modal Streamlit application leveraging Google's Gemini models for text generation, Pollinations.ai for image generation, and Hugging Face Spaces for music and video generation.

## Features

- **Text:** Conversational AI powered by Google Gemini (Supports Gemini 1.5 Flash & Pro).
- **Vision:** Multi-modal support (upload images + ask questions).
- **Image Generation:** Create images using Pollinations.ai.
- **Music Generation:** Generate music using MusicGen (via Hugging Face).
- **Video Generation:** Create short videos from text prompts (via Hugging Face).

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repo_url>
   cd gemini_bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   - Create a `.env` file based on `.env.example`.
   - Add your [Google AI Studio API Key](https://aistudio.google.com/app/apikey) as `GOOGLE_API_KEY`.

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

## Structure

- `app.py`: Main entry point for the Streamlit interface.
- `modules/`: Contains separate modules for text, image, music, and video generation logic.
- `utils/`: Helper functions.

## Notes

- Ensure you have a stable internet connection as all generations rely on external APIs.
- The `gradio_client` is used to interface with Hugging Face Spaces. Availability of specific Spaces may vary.
