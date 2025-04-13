import json
import os
from typing import Dict, List, Union

from base import FileHandler
from vacancy import Vacancy


class JSONFileHandler(FileHandler):
    """Класс для работы с JSON-файлом, содержащим вакансии."""

    __slots__ = "__filename"

    def __init__(self, filename: str = "vacancies.json") -> None:
        """
        Инициализирует обработчик JSON-файла для хранения вакансий.
        Если файл не существует, он создаётся.

        :param filename: Имя JSON-файла (по умолчанию — vacancies.json в папке 'data').
        """
        path_module = os.path.abspath(os.path.dirname(__file__))
        path_project = os.path.dirname(path_module)

        # Папка 'data' в корне проекта
        data_dir = os.path.join(path_project, "data")
        os.makedirs(data_dir, exist_ok=True)

        # Полный путь к JSON-файлу
        self.__filename = os.path.join(data_dir, filename)
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Метод для добавления вакансии в файл, избегая дублирования.

        :param vacancy: Объект вакансии.
        """
        data = self._load_data()
        vacancy_dict = {
            "title": vacancy.title,
            "salary": vacancy.salary,
            "description": vacancy.description,
            "city": vacancy.city,
            "url": vacancy.url,
        }
        if vacancy_dict not in data:
            data.append(vacancy_dict)
            self._save_data(data)

    def get_vacancies(self, **criteria: Union[str, int]) -> List[Dict]:
        """
        Метод для получения вакансий из файла по переданным критериям.

        :param criteria: Параметры для фильтрации (ключ — поле, значение — значение).
        :return: Список словарей с данными о вакансиях.
        """
        data = self._load_data()

        result = []
        for vacancy in data:
            if all(vacancy.get(key) == value for key, value in criteria.items()):
                result.append(vacancy)
        return result

    def delete_vacancy(self, title: str) -> None:
        """
        Метод для удаления вакансии из файла по названию.

        :param title: Название вакансии.
        """
        data = self._load_data()
        updated_data = [vacancy for vacancy in data if vacancy.get("title") != title]
        self._save_data(updated_data)

    def _load_data(self) -> List[Dict]:
        """
        Метод для загрузки данных о вакансиях из файла.

        :return: Список словарей с данными о вакансиях.
        """
        with open(self.__filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_data(self, data: List[Dict]) -> None:
        """Метод для сохранения данных о вакансиях в файл.

        :param data: Список словарей с данными о вакансиях.
        """
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
