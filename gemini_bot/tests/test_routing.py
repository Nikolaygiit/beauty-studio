from modules.routing import get_route

def test_get_route():
    # Test text
    assert get_route("привет как дела") == "text"
    assert get_route("расскажи сказку") == "text"

    # Test image
    assert get_route("нарисуй кота") == "image"
    assert get_route("красивое фото заката") == "image"
    assert get_route("покажи изображение природы") == "image"
    assert get_route("сделай картинку") == "image"

    # Test music
    assert get_route("создай музыку") == "music"
    assert get_route("спой песню") == "music"
    assert get_route("крутой трек") == "music"

    # Test video
    assert get_route("сними видео") == "video"
    assert get_route("короткий ролик") == "video"

    # Test case insensitivity and boundaries
    assert get_route("НАРИСУЙ собаку") == "image"
    assert get_route("включи МУЗЫКУ пожалуйста") == "music"
