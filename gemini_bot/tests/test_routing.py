from modules.routing import get_media_route

def test_get_media_route_image():
    assert get_media_route("нарисуй кота") == "image"
    assert get_media_route("сделай фото заката") == "image"
    assert get_media_route("сгенерируй картинку дома") == "image"
    assert get_media_route("покажи изображение леса") == "image"

def test_get_media_route_music():
    assert get_media_route("напиши музыку для сна") == "music"
    assert get_media_route("сочини веселую песню") == "music"
    assert get_media_route("крутой трек") == "music"
    assert get_media_route("много песен") == "music"

def test_get_media_route_video():
    assert get_media_route("создай видео природы") == "video"
    assert get_media_route("смешной ролик") == "video"

def test_get_media_route_text():
    assert get_media_route("привет, как дела?") == "text"
    assert get_media_route("что такое фотосинтез") == "text" # 'фото' inside another word
    assert get_media_route("расскажи про музыкантов") == "text" # No matching word boundary
