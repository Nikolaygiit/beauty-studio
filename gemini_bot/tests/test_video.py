import pytest
from modules.video import get_video_client, generate_video

def test_get_video_client_success(mocker):
    mock_client = mocker.patch("modules.video.Client")
    client, err = get_video_client()
    mock_client.assert_called_once_with("damo-vilab/modelscope-text-to-video-synthesis")
    assert err is None
    assert client is not None

def test_get_video_client_failure(mocker):
    import streamlit as st
    st.cache_resource.clear()

    mocker.patch("modules.video.Client", side_effect=Exception("Timeout"))
    client, err = get_video_client()
    assert client is None
    assert "Ошибка инициализации видео" in err

def test_generate_video_success(mocker):
    mock_get_client = mocker.patch("modules.video.get_video_client")
    mock_client_instance = mocker.MagicMock()
    mock_client_instance.predict.return_value = ["/path/to/video.mp4"]
    mock_get_client.return_value = (mock_client_instance, None)

    path, err = generate_video("cat running")

    mock_client_instance.predict.assert_called_once_with(
        "cat running",
        -1,
        16,
        25,
        api_name="/generate_video"
    )
    assert path == "/path/to/video.mp4"
    assert err is None

def test_generate_video_error(mocker):
    mock_get_client = mocker.patch("modules.video.get_video_client")
    mock_client_instance = mocker.MagicMock()
    mock_client_instance.predict.side_effect = Exception("Model error")
    mock_get_client.return_value = (mock_client_instance, None)

    path, err = generate_video("error prompt")
    assert path is None
    assert "Ошибка генерации видео" in err
