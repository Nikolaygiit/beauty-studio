# Gemini Ultimate Bot 🤖

This is a comprehensive AI bot built with Streamlit, powered by Google's Gemini models and other generative AI tools.

## Features 🚀

-   **Chat 💬:** Converse with **Gemini 1.5 Flash**. Supports multi-turn conversations and image analysis (multimodal).
-   **Image Generation 🖼️:** Generate high-quality images using **Pollinations.ai** (Models: Flux, Turbo, Stable Diffusion). No API key required for this feature.
-   **Music Generation 🎵:** Create music tracks using **MusicGen** (via Hugging Face Spaces).
-   **Video Generation 🎥:** Generate short videos using **ModelScope** (via Hugging Face Spaces).

## Installation 🛠️

1.  Navigate to the project directory:
    ```bash
    cd gemini_bot
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage ▶️

1.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2.  Open your browser at the provided local URL (usually `http://localhost:8501`).

3.  **API Key:**
    -   For **Chat** functionality, you need a **Google API Key**.
    -   Get it for free here: [Google AI Studio](https://aistudio.google.com/).
    -   Enter the key in the sidebar when prompted.

## Notes 📝

-   **Image Generation** is fast and free.
-   **Music and Video Generation** rely on public Hugging Face Spaces. These can be slower or have queues during peak usage times.
-   The chat history is maintained within the session but clears if you refresh the page or change the API key.
