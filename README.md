# Gemini Bot

A fully functional, browser-based AI chat bot powered by Google's Gemini models. This application allows you to chat with Gemini 1.5 Flash or Pro, analyze images, video, and audio files, and generate text and code.

## Features

*   **Chat Interface:** Clean, modern, dark-themed chat interface.
*   **Multimodal Support:** Upload and analyze images, videos, and audio files alongside your text prompts.
*   **Model Selection:** Switch between Gemini 1.5 Flash (faster, lower cost) and Gemini 1.5 Pro (more capable).
*   **History:** Session-based chat history (cleared on refresh for privacy in this demo version).
*   **Secure API Key Storage:** Your Google API key is stored locally in your browser's `localStorage` and never sent to a third-party server (only directly to Google's API).
*   **Markdown Support:** Responses are formatted with Markdown (bold, code blocks, etc.).
*   **Responsive Design:** Works on desktop and mobile.

## Getting Started

### Prerequisites

You need a Google AI Studio API Key.
1.  Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Create an API key.

### Installation

1.  Clone this repository or download the files.
2.  Open `index.html` in your web browser.
3.  Click the "Settings" icon (gear) in the sidebar.
4.  Enter your API Key and click "Save".

### Usage

1.  Type your message in the input box and press Enter or click the send button.
2.  To upload a file (image, video, audio), click the paperclip icon.
3.  To start a new chat, click "New Chat" in the sidebar.
4.  To change the model, go to Settings and select your preferred model.

## Technologies Used

*   **HTML5/CSS3:** Core structure and styling.
*   **JavaScript (ES6+):** Application logic.
*   **Google Generative AI SDK:** Integration with Gemini API via CDN.
*   **FontAwesome:** Icons.

## Notes

*   Large video/audio files (> 20MB) are restricted in this client-side demo to prevent browser crashes.
*   This is a client-side only application. No backend server is required.
