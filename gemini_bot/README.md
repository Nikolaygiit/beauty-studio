# Gemini Ultimate Bot

An all-in-one AI bot capable of generating text, images, music, and videos using Google Gemini and Hugging Face models.

## Features

- **Text Chat**: Powered by Google Gemini 1.5 Flash.
- **Image Generation**: Powered by Pollinations.ai.
- **Music Generation**: Powered by Facebook MusicGen (via Hugging Face).
- **Video Generation**: Powered by DAMO Text-to-Video (via Hugging Face).

## Setup

1. Clone the repository.
2. Navigate to the `gemini_bot` directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` and add your API keys:
   - `GOOGLE_API_KEY`: Get it from [Google AI Studio](https://aistudio.google.com/).
   - `HF_TOKEN` (Optional): Get it from [Hugging Face](https://huggingface.co/settings/tokens) to avoid rate limits on music/video generation.

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

## Note

- Music and Video generation may take some time depending on the load on Hugging Face Spaces.
- Image generation is instant via Pollinations.ai.
