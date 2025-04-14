from typing import Union

from src.currency import CurrencyConverter


class Vacancy:
    """
    Класс для представления вакансии.
    """

    __slots__ = ("__title", "__salary", "__description", "__city", "__url")
    _converter = CurrencyConverter()

    def __init__(self, title: str, salary: Union[dict, int, None], description: str, city: str, url: str) -> None:
        """
        Инициализирует объект вакансии.

        :param title: Название вакансии.
        :param salary: Зарплата (если не указана или некорректна, устанавливается в 0).
        :param description: Описание или требования.
        :param city: Город.
        :param url: Ссылка на вакансию.
        """
        self.__title = title.strip() if title else "Без названия"
        self.__salary = self.__parse_salary(salary)
        self.__description = description.strip() if description else "Описание отсутствует"
        self.__city = city.strip() if city else "Город не указан"
        self.__url = url.strip() if url else "Ссылка не указана"

    @staticmethod
    def __parse_salary(salary: Union[dict, int, None]) -> int:
        """
        Метод для обработки зарплаты из API.

        - Если salary — число и > 0, возвращается как есть.
        - Если salary — словарь:
            - если есть и 'from', и 'to' — возвращается среднее арифметическое.
            - если только 'from' — возвращается 'from'.
            - если только 'to' — возвращается 'to'.
        - Если salary отсутствует или некорректно — возвращается 0.

        :param salary: Зарплата вакансии (dict, int или None).
        :return: Обработанная зарплата (int).
        """
        if isinstance(salary, int) and salary > 0:
            return salary
        if isinstance(salary, dict):
            _from = salary.get("from")
            _to = salary.get("to")
            currency = salary.get("currency", "RUR")
            if _from and _to:
                avg = (_from + _to) // 2
                return Vacancy._converter.convert_to_rub(avg, currency)
            if _from:
                return Vacancy._converter.convert_to_rub(_from, currency)
            if _to:
                return Vacancy._converter.convert_to_rub(_to, currency)
        return 0  # Если salary = None или некорректно

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта Vacancy."""
        salary_text = f"{self.__salary} ₽" if self.__salary > 0 else "Зарплата не указана"
        return f"{self.__title} | {self.__city} | {salary_text} — {self.__url}"

    def __lt__(self, other: object) -> bool:
        """Сравнение вакансий по зарплате (меньше)."""
        if not isinstance(other, Vacancy):
            raise TypeError("Сравнение возможно только между объектами класса 'Vacancy'")
        return self.__salary < other.__salary

    def __eq__(self, other: object) -> bool:
        """Сравнение вакансий по зарплате (равны)."""
        if not isinstance(other, Vacancy):
            raise TypeError("Сравнение возможно только между объектами класса 'Vacancy'")
        return self.__salary == other.__salary

    def __gt__(self, other: object) -> bool:
        """Сравнение вакансий по зарплате (больше)."""
        if not isinstance(other, Vacancy):
            raise TypeError("Сравнение возможно только между объектами класса 'Vacancy'")
        return self.__salary > other.__salary

    @property
    def title(self) -> str:
        """Геттер для получения названия вакансии."""
        return self.__title

    @property
    def salary(self) -> int:
        """Геттер для получения зарплаты вакансии."""
        return self.__salary

    @property
    def description(self) -> str:
        """Геттер для получения описания вакансии."""
        return self.__description

    @property
    def city(self) -> str:
        """Геттер для получения города вакансии."""
        return self.__city

    @property
    def url(self) -> str:
        """Геттер для получения ссылки на вакансию."""
        return self.__url
