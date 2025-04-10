from abc import ABC, abstractmethod
from typing import Dict, List

import requests


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервиса вакансий."""

    @abstractmethod
    def _connect(self) -> None:
        """Абстрактный метод для отправки запроса на базовый URL и проверки статус-кода."""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict]:
        """
        Абстрактный метод для получения списка вакансий по ключевому слову.

        :param keyword: Ключевое слово.
        :return: Список словарей с данными.
        """
        pass


class HeadHunterAPI(VacancyAPI):

    def __init__(self) -> None:
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "vacancy-tracker-app"}

    def _connect(self) -> None:
        """Проверка доступности API по базовому URL."""
        response = requests.get(self.__base_url, headers=self.__headers)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f"Ошибка подключения: {response.status_code}")

    def get_vacancies(self, keyword: str) -> List[Dict]:
        """
        Абстрактный метод для получения списка вакансий по ключевому слову.

        :param keyword: Ключевое слово.
        :return: Список словарей с данными.
        """
        self._connect()  # Проверяем наличие соединения с API

        vacancies = []
        params = {"text": keyword, "page": 0, "per_page": 100}

        while params["page"] < 20:
            response = requests.get(self.__base_url, headers=self.__headers, params=params)
            if response.status_code != 200:
                break
            items = response.json().get("items", [])
            if not items:
                break
            vacancies.extend(items)
            params["page"] += 1

        return vacancies
