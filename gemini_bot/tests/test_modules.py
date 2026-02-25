import unittest
import os
import sys

# Add project root to path BEFORE imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from gemini_bot.modules import image, music, video, text

class TestModules(unittest.TestCase):
    def test_image_generation(self):
        url = image.generate_image("test prompt")
        self.assertTrue(url.startswith("https://image.pollinations.ai"))
        # Check encoding logic
        # quote("test prompt") -> "test%20prompt"
        self.assertIn("test%20prompt", url)

    def test_text_import(self):
        self.assertTrue(callable(text.generate_response))
        self.assertTrue(callable(text.configure_api))

    def test_music_import(self):
        self.assertTrue(callable(music.generate_music))

    def test_video_import(self):
        self.assertTrue(callable(video.generate_video))

if __name__ == '__main__':
    unittest.main()
