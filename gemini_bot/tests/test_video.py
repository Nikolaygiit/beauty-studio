import pytest
from modules.video import generate_video

def test_generate_video_success_string(mocker):
    class MockClient:
        def predict(self, prompt, seed, num_frames, num_inference_steps, api_name):
            assert prompt == "test prompt"
            assert seed == -1
            assert num_frames == 16
            assert num_inference_steps == 25
            assert api_name == "/generate_video"
            return "path/to/video.mp4"

    mocker.patch('modules.video.get_video_client', return_value=MockClient())

    file_path, err = generate_video("test prompt")

    assert err is None
    assert file_path == "path/to/video.mp4"

def test_generate_video_success_dict(mocker):
    class MockClient:
        def predict(self, *args, **kwargs):
            return {'video': "path/to/video2.mp4"}

    mocker.patch('modules.video.get_video_client', return_value=MockClient())

    file_path, err = generate_video("test prompt")

    assert err is None
    assert file_path == "path/to/video2.mp4"

def test_generate_video_client_error(mocker):
    mocker.patch('modules.video.get_video_client', return_value="Ошибка инициализации...")

    file_path, err = generate_video("test prompt")

    assert file_path is None
    assert err == "Ошибка инициализации..."

def test_generate_video_predict_valueerror(mocker):
    class MockClient:
        def predict(self, *args, **kwargs):
            raise ValueError("Bad values")

    mocker.patch('modules.video.get_video_client', return_value=MockClient())

    file_path, err = generate_video("test prompt")

    assert file_path is None
    assert err == "Ошибка значения при генерации видео: Bad values"

def test_generate_video_predict_runtimeerror(mocker):
    class MockClient:
        def predict(self, *args, **kwargs):
            raise RuntimeError("Runtime error")

    mocker.patch('modules.video.get_video_client', return_value=MockClient())

    file_path, err = generate_video("test prompt")

    assert file_path is None
    assert err == "Ошибка времени выполнения при генерации видео: Runtime error"
