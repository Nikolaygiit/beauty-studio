# Gemini Ultimate Bot

An all-in-one AI assistant capable of generating text, images, music, and videos.

## Features

- **Text**: Powered by Google Gemini 1.5 Flash.
- **Image**: Powered by Pollinations.ai.
- **Music**: Powered by MusicGen (Hugging Face Space).
- **Video**: Powered by ModelScope (Hugging Face Space).

## Installation

1. Navigate to the `gemini_bot` directory:
   ```bash
   cd gemini_bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application from the `gemini_bot` directory:
   ```bash
   streamlit run app.py
   ```
   Or from the root directory:
   ```bash
   streamlit run gemini_bot/app.py
   ```
2. Open your browser at the provided URL (usually `http://localhost:8501`).
3. Enter your Google API Key in the sidebar.
4. Start chatting!

### Commands

- Just type to chat (Text generation).
- Type "draw [something]" or "generate image of [something]" for images.
- Type "generate music [description]" for music.
- Type "generate video [description]" for video.

## Notes

- **Video Generation**: The video generation service (ModelScope) may be busy or unavailable at times.
- **Music Generation**: Music generation can take up to a minute.
- **API Key**: A Google API Key is required for text generation. You can get one from [Google AI Studio](https://makersuite.google.com/app/apikey).
