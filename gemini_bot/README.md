# Gemini Ultimate Bot

A powerful bot built with Streamlit that leverages:
- **Gemini 1.5 Flash** for text generation.
- **Pollinations.ai** for image generation.
- **MusicGen** for music generation (via Hugging Face Spaces).
- **ModelScope** for video generation (via Hugging Face Spaces).

## Installation

1.  Clone the repository and navigate to `gemini_bot/`.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up your environment variables:
    - Copy `.env.example` to `.env`.
    - Fill in your `GOOGLE_API_KEY`.
    - (Optional) Add `HF_TOKEN` if you have a Hugging Face token for better access to Spaces.

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## Note on Hugging Face Spaces

The Music and Video generation features rely on public Hugging Face Spaces (`facebook/MusicGen` and `damo-vilab/modelscope-damo-text-to-video-synthesis`). These spaces may be:
- Busy (Queue full)
- Temporarily down (Runtime Error)
- Changed or deprecated

If you encounter errors, check the logs or try again later. You can also modify `app.py` to point to your own private Spaces if you have them.
