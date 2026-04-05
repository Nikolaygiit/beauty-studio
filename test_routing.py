from gemini_bot.app import route_request

def test_routing():
    assert route_request("нарисуй кота") == "image"
    assert route_request("сделай фото") == "image"
    assert route_request("красивое изображение") == "image"

    assert route_request("какая классная музыка") == "music"
    assert route_request("это хорошая песня") == "music"
    assert route_request("новый трек") == "music"

    assert route_request("сделай видео") == "video"
    assert route_request("короткий ролик") == "video"

    assert route_request("расскажи анекдот") == "text"
    assert route_request("как дела?") == "text"

    print("All routing tests passed!")

if __name__ == "__main__":
    test_routing()
