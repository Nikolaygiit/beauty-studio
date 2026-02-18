# Gemini Ultimate Bot

A powerful AI bot built with Streamlit that integrates multiple generative AI models.

## Features

- **Text & Chat:** Powered by Google's **Gemini 1.5 Flash** model. Supports multi-turn conversations.
- **Image Generation:** Powered by **Pollinations.ai**. No API key required for images.
- **Music Generation:** Powered by **Facebook MusicGen** via Hugging Face Spaces.
- **Video Generation:** Powered by **ModelScope Text-to-Video** via Hugging Face Spaces.

## Prerequisites

- Python 3.9+
- A Google Cloud API Key for Gemini.
- (Optional) A Hugging Face Token for higher rate limits or accessing gated spaces.

## Installation

1. Navigate to the project directory:
   ```bash
   cd gemini_bot
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. In the application sidebar:
   - Enter your **Google API Key**.
   - (Optional) Enter your **Hugging Face Token**.

3. Use the tabs to switch between Chat, Image, Music, and Video generation.

## Troubleshooting

- **Music/Video Generation Failed:**
  - Hugging Face Spaces can sometimes be busy, down, or rate-limited.
  - If you see a "Runtime Error" or "401 Client Error", try providing a valid **Hugging Face Token** in the sidebar.
  - Some spaces might require you to accept their license on the Hugging Face website.

## Dependencies

- streamlit
- google-generativeai
- python-dotenv
- requests
- gradio_client
- Pillow
