from typing import Dict, List

import requests
from tqdm import tqdm

from src.base import VacancyAPI


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
        max_pages = 20

        for _ in tqdm(range(max_pages), desc="Получение данных"):
            response = requests.get(self.__base_url, headers=self.__headers, params=params)
            if response.status_code != 200:
                break
            items = response.json().get("items", [])
            if not items:
                break
            vacancies.extend(items)
            params["page"] += 1

        return vacancies
