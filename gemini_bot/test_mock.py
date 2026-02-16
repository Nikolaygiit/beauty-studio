import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core import GeminiHandler
import media

class TestGeminiBot(unittest.TestCase):
    @patch('core.genai')
    def test_gemini_handler_init(self, mock_genai):
        handler = GeminiHandler(api_key="test_key")
        mock_genai.configure.assert_called_with(api_key="test_key")
        mock_genai.GenerativeModel.assert_called_with('gemini-1.5-flash')

    @patch('core.genai')
    def test_generate_content(self, mock_genai):
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_response = MagicMock()
        mock_response.text = "Hello"
        mock_model.generate_content.return_value = mock_response

        handler = GeminiHandler(api_key="test_key")
        result = handler.generate_content("Hi")
        self.assertEqual(result, "Hello")
        mock_model.generate_content.assert_called_with("Hi")

    @patch('media.requests.get')
    def test_generate_image(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"image_data"
        mock_get.return_value = mock_response

        result = media.generate_image("test prompt")
        self.assertEqual(result, b"image_data")

    @patch('media.Client')
    @patch('media.os.path.exists')
    def test_generate_music(self, mock_exists, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        # Mock exists to return True for the file
        mock_exists.side_effect = lambda x: x == "audio.wav"

        mock_client.predict.return_value = ["dummy", "audio.wav"]

        result = media.generate_music("test music")
        self.assertEqual(result, "audio.wav")

if __name__ == '__main__':
    unittest.main()
