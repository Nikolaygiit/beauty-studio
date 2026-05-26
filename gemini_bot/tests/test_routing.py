from app import matches_keyword

def test_matches_keyword_image():
    keywords = ['нарисуй', 'фото', 'изображение']
    assert matches_keyword("Нарисуй мне кота", keywords) is True
    assert matches_keyword("покажи фото собаки", keywords) is True
    assert matches_keyword("сгенерируй изображение леса", keywords) is True
    assert matches_keyword("напиши сказку", keywords) is False

def test_matches_keyword_music():
    keywords = ['музык', 'песн', 'песен', 'трек']
    assert matches_keyword("сделай музыку", keywords) is True
    assert matches_keyword("включи песню", keywords) is True
    assert matches_keyword("спой песенку", keywords) is True
    assert matches_keyword("классный трек", keywords) is True
    assert matches_keyword("напиши текст", keywords) is False

def test_matches_keyword_video():
    keywords = ['видео', 'ролик']
    assert matches_keyword("сними видео", keywords) is True
    assert matches_keyword("короткий ролик", keywords) is True
    assert matches_keyword("напиши письмо", keywords) is False
