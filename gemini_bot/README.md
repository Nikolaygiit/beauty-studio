# Gemini Ultimate Bot

An all-in-one AI assistant powered by Gemini 1.5 Flash and various Hugging Face Spaces.

## Features
- **Chat:** Conversational AI using Google's Gemini 1.5 Flash model.
- **Image Generation:** Create images from text descriptions using Pollinations.ai.
- **Music Generation:** Generate music using `facebook/MusicGen` (via `sanchit-gandhi/musicgen-streaming` space).
- **Video Generation:** Generate videos using `damo-vilab/modelscope-text-to-video-synthesis`.

## Setup

1. **Navigate to the directory:**
   ```bash
   cd gemini_bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys:**
   - You need a Google API Key from [Google AI Studio](https://aistudio.google.com/).
   - Optionally, a Hugging Face Token (Read access) is recommended for better reliability with Spaces.

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Environment Variables
You can also set environment variables in a `.env` file:
```
GOOGLE_API_KEY=your_google_api_key
HF_TOKEN=your_hugging_face_token
```

## Troubleshooting
- If Music or Video generation fails with "RUNTIME_ERROR" or "401 Client Error", the underlying Hugging Face Space might be down or require authentication.
- You can try changing the space name in `modules/video.py` or `modules/music.py` via code or `VIDEO_SPACE_NAME` env var if you find a working alternative.
