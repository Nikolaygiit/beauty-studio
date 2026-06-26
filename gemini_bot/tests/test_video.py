from modules.video import get_video_client, generate_video

def test_get_video_client_success(mocker):
    import streamlit as st
    st.cache_resource.clear()

    mock_client = mocker.patch("modules.video.Client")
    client, error = get_video_client()

    assert client is not None
    assert error is None
    mock_client.assert_called_once_with("damo-vilab/modelscope-text-to-video-synthesis")

def test_get_video_client_error(mocker):
    import streamlit as st
    st.cache_resource.clear()

    mocker.patch("modules.video.Client", side_effect=Exception("Connection error"))
    client, error = get_video_client()

    assert client is None
    assert "Ошибка инициализации сервиса видео" in error

def test_generate_video_no_client():
    path, error = generate_video("test", None)
    assert path is None
    assert error == "Клиент видео не инициализирован."

def test_generate_video_success(mocker):
    mock_client = mocker.Mock()
    mock_client.predict.return_value = "path/to/video.mp4"

    path, error = generate_video("ocean waves", mock_client)

    assert path == "path/to/video.mp4"
    assert error is None
    mock_client.predict.assert_called_once_with(
        "ocean waves",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

def test_generate_video_value_error(mocker):
    mock_client = mocker.Mock()
    mock_client.predict.side_effect = ValueError("Invalid parameter")

    path, error = generate_video("test", mock_client)
    assert path is None
    assert "Ошибка параметров видео" in error

def test_generate_video_runtime_error(mocker):
    mock_client = mocker.Mock()
    mock_client.predict.side_effect = RuntimeError("GPU out of memory")

    path, error = generate_video("test", mock_client)
    assert path is None
    assert "Ошибка выполнения видео" in error

def test_generate_video_generic_error(mocker):
    mock_client = mocker.Mock()
    mock_client.predict.side_effect = Exception("Unknown")

    path, error = generate_video("test", mock_client)
    assert path is None
    assert "Неизвестная ошибка" in error
