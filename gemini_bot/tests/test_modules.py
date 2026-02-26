import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add gemini_bot to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from gemini_bot.modules.image import ImageGenerator
from gemini_bot.modules.text import GeminiText

class TestImageGenerator(unittest.TestCase):
    def test_generate_image(self):
        generator = ImageGenerator()
        prompt = "a cute cat"
        url = generator.generate_image(prompt)
        expected_url = "https://image.pollinations.ai/prompt/a%20cute%20cat"
        self.assertEqual(url, expected_url)

class TestGeminiText(unittest.TestCase):
    def test_init_without_api_key(self):
        gemini = GeminiText(api_key="")
        self.assertIsNone(gemini.model)
        self.assertIsNone(gemini.chat)
        response = gemini.send_message("hello")
        self.assertEqual(response, "Please enter your Google API Key in the sidebar.")

    @patch('gemini_bot.modules.text.genai')
    def test_init_with_api_key(self, mock_genai):
        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat

        gemini = GeminiText(api_key="fake_key")

        mock_genai.configure.assert_called_with(api_key="fake_key")
        mock_genai.GenerativeModel.assert_called_with('gemini-1.5-flash')
        mock_model.start_chat.assert_called_with(history=[])

        self.assertEqual(gemini.model, mock_model)
        self.assertEqual(gemini.chat, mock_chat)

    @patch('gemini_bot.modules.text.genai')
    def test_send_message(self, mock_genai):
        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat

        # Mock response
        mock_response = MagicMock()
        mock_chat.send_message.return_value = mock_response

        gemini = GeminiText(api_key="fake_key")
        response = gemini.send_message("hello")

        mock_chat.send_message.assert_called_with("hello", stream=True)
        self.assertEqual(response, mock_response)

if __name__ == '__main__':
    unittest.main()
