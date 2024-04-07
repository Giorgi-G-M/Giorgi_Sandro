import pytest
from unittest.mock import patch
from money import get_data, get_rate, get_currencies  # Replace 'your_script' with the name of your script file

@patch('money.requests.get')
def test_get_data(mock_get):
    mock_get.return_value.json.return_value = [{"currencies": [{"code": "USD", "rate": 3.1}]}]
    data = get_data()
    assert data == [{"currencies": [{"code": "USD", "rate": 3.1}]}]

@patch('money.get_data')
def test_get_currencies(mock_get_data):
    mock_get_data.return_value = [{"currencies": [{"code": "USD"}, {"code": "EUR"}]}]
    currencies = get_currencies()
    assert "USD" in currencies
    assert "EUR" in currencies
    assert len(currencies) == 3


@patch('money.get_data')
def test_get_rate(mock_get_data):
    mock_get_data.return_value = [{"currencies": [{"code": "USD", "rate": 3.1}, {"code": "EUR", "rate": 3.5}]}]
    rates = get_rate()
    assert {"USD": 3.1} in rates
    assert {"EUR": 3.5} in rates
