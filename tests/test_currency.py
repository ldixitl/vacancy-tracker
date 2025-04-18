from typing import Any
from unittest.mock import MagicMock, patch

import requests

from src.currency import CurrencyConverter


@patch("src.currency.requests.get")
def test_load_rates_success(mock_get: Any) -> None:
    """Проверяет успешную загрузку курсов валют."""
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {"rates": {"USD": 100.0, "EUR": 110.0}})

    CurrencyConverter.load_rates()
    assert CurrencyConverter._rates["USD"] == 100.0
    assert CurrencyConverter._rates["EUR"] == 110.0


@patch("src.currency.requests.get")
def test_load_rates_failure(mock_get: Any) -> None:
    """Проверяет обработку ошибки при загрузке курсов валют."""
    mock_get.side_effect = requests.RequestException("Ошибка сети")
    CurrencyConverter.load_rates()
    assert CurrencyConverter._rates == {}


@patch("src.currency.requests.get")
def test_convert_to_rub(mock_get: Any) -> None:
    """Проверяет конвертацию суммы в рубли."""
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {"rates": {"USD": 100.0}})
    converter = CurrencyConverter()
    assert converter.convert_to_rub(200, "USD") == 2
    assert converter.convert_to_rub(200, "RUB") == 200
    assert converter.convert_to_rub(200, "RUR") == 200
    assert converter.convert_to_rub(200, "") == 200
    assert converter.convert_to_rub(200, "EUR") == 0
