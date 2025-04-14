from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.external_api import HeadHunterAPI


@patch("src.external_api.requests.get")
def test_connect_success(mock_get: Any) -> None:
    """Проверка успешного подключения к API."""
    mock_get.return_value.status_code = 200
    api = HeadHunterAPI()
    api._connect()
    mock_get.assert_called_once_with("https://api.hh.ru/vacancies", headers={"User-Agent": "vacancy-tracker-app"})


@patch("src.external_api.requests.get")
def test_connect_failure(mock_get: Any) -> None:
    """Проверка обработки ошибки подключения (код != 200)."""
    mock_get.return_value.status_code = 500
    api = HeadHunterAPI()
    with pytest.raises(requests.exceptions.HTTPError):
        api._connect()


@patch("src.external_api.requests.get")
def test_get_vacancies_success(mock_get):
    """Тест успешного получения нескольких страниц вакансий."""
    # Мокаем _connect() и 2 страницы вакансий, затем пустую
    mock_get.side_effect = [
        MagicMock(status_code=200),  # _connect()
        MagicMock(status_code=200, json=lambda: {"items": [{"id": "v1"}, {"id": "v2"}]}),
        MagicMock(status_code=200, json=lambda: {"items": [{"id": "v3"}, {"id": "v4"}]}),
        MagicMock(status_code=200, json=lambda: {"items": []}),
    ]

    api = HeadHunterAPI()
    vacancies = api.get_vacancies("Python")

    assert len(vacancies) == 4
    assert vacancies[0]["id"] == "v1"
    assert vacancies[3]["id"] == "v4"


@patch("src.external_api.requests.get")
def test_get_vacancies_empty_result(mock_get):
    """Тест, если API сразу возвращает пустой список."""
    mock_get.side_effect = [
        MagicMock(status_code=200),  # _connect()
        MagicMock(status_code=200, json=lambda: {"items": []}),
    ]

    api = HeadHunterAPI()
    result = api.get_vacancies("NoResults")
    assert result == []


@patch("src.external_api.requests.get")
def test_get_vacancies_api_failure(mock_get: Any) -> None:
    """Проверка, что цикл останавливается при ошибке ответа от API (status_code != 200)."""
    mock_get.side_effect = [
        MagicMock(status_code=200),  # _connect()
        MagicMock(status_code=500),  # первый запрос за вакансиями
    ]

    api = HeadHunterAPI()
    result = api.get_vacancies("Python")
    assert result == []
