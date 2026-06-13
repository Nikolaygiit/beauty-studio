import pytest
from modules.music import generate_music

def test_generate_music_success(mocker):
    class MockClient:
        def predict(self, text_prompt, audio_length_in_s, play_steps_in_s, seed, api_name):
            assert text_prompt == "test prompt"
            assert audio_length_in_s == 15
            assert play_steps_in_s == 1.5
            assert seed == 0
            assert api_name == "/generate_audio"
            return "path/to/audio.wav"

    mocker.patch('modules.music.get_music_client', return_value=MockClient())

    file_path, err = generate_music("test prompt")

    assert err is None
    assert file_path == "path/to/audio.wav"

def test_generate_music_client_error(mocker):
    mocker.patch('modules.music.get_music_client', return_value="Ошибка инициализации...")

    file_path, err = generate_music("test prompt")

    assert file_path is None
    assert err == "Ошибка инициализации..."

def test_generate_music_predict_error(mocker):
    class MockClient:
        def predict(self, *args, **kwargs):
            raise Exception("Prediction error")

    mocker.patch('modules.music.get_music_client', return_value=MockClient())

    file_path, err = generate_music("test prompt")

    assert file_path is None
    assert err == "Ошибка генерации музыки: Prediction error"
