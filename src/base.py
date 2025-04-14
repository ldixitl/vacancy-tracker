from abc import ABC, abstractmethod
from typing import Dict, List, Union

from src.vacancy import Vacancy


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


class FileHandler(ABC):
    """Абстрактный класс для работы с файлами вакансий."""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Абстрактный метод для добавления вакансии в файл."""
        pass

    @abstractmethod
    def get_vacancies(self, **criteria: Union[str, int]) -> List[Dict]:
        """Абстрактный метод для получения вакансий из файла."""
        pass

    @abstractmethod
    def delete_vacancy(self, title: str) -> None:
        """Абстрактный метод для удаления вакансии из файла по названию."""
        pass
