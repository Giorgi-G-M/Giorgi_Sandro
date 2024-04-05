import pytest
from weather import get_info, sun_rise, sun_set, degrees_to_direction, weather_checker, fahrenheit_converter, celsius_converter

def test_get_info():
    data = {"main": {"humidity": 92}, "weather": [{"description": "clear sky"}]}
    expected_output = (92, "clear sky")
    assert get_info(data) == expected_output

def test_sun_rise():
    data = {"sys": {"sunrise": 1560281377}}
    expected_output = "2019-06-11 23:29:37" 
    assert str(sun_rise(data)) == expected_output


def test_sun_set():
    data = {"sys": {"sunset": 1560333478}}
    expected_output = "2019-06-12 13:57:58" 
    assert str(sun_set(data)) == expected_output

def test_degrees_to_direction():
    data = {"wind": {"deg": 90}}
    expected_output = "East-southeast" 
    assert degrees_to_direction(data) == expected_output

def test_weather_checker():
    data = {"weather": [{"description": "rain"}]}
    expected_output = "take a ambrella"
    assert weather_checker(data) == expected_output

def test_fahrenheit_converter():
    data = {"main": {"temp": 280}}
    expected_output = 44
    assert fahrenheit_converter(data) == expected_output

def test_celsius_converter():
    data = {"main": {"temp": 280}}
    expected_output = 7
    assert celsius_converter(data) == expected_output
