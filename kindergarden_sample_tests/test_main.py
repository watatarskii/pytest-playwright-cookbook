def test_get_weather():
    from kundergarden_sample_tests.main import get_weather
    
    assert get_weather(25) == "It's hot!"
    assert get_weather(15) == "It's cold!"
    assert get_weather(30) == "It's cold!"