class Vacancy:
    """
    Класс для представления вакансии.
    """

    __slots__ = ("__title", "__salary", "__description", "__city", "__url")

    def __init__(self, title: str, salary: int, description: str, city: str, url: str) -> None:
        """
        Инициализирует объект вакансии.

        :param title: Название вакансии.
        :param salary: Зарплата (если не указана или некорректна, устанавливается в 0).
        :param description: Описание или требования.
        :param city: Город.
        :param url: Ссылка на вакансию.
        """
        self.__title = title.strip() if title else "Без названия"
        self.__salary = salary if isinstance(salary, int) and salary > 0 else 0
        self.__description = description.strip() if description else "Описание отсутствует"
        self.__city = city.strip() if city else "Город не указан"
        self.__url = url.strip() if url else "Ссылка не указана"

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта Vacancy."""
        salary_text = f"{self.__salary} ₽" if self.__salary > 0 else "Зарплата не указана"
        return f"{self.__title} ({salary_text}) — {self.__url}"

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
