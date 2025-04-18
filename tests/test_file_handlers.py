import pytest

from src.file_handlers import JSONFileHandler
from src.vacancy import Vacancy


@pytest.fixture
def temp_handler(tmp_path) -> JSONFileHandler:
    """Создаёт временный JSON-файл и возвращает экземпляр JSONFileHandler."""
    test_file = tmp_path / "test_vacancies.json"
    return JSONFileHandler(filename=str(test_file))


def test_add_and_get_vacancy(temp_handler: JSONFileHandler) -> None:
    """Проверка добавления и получения вакансии."""
    vacancy = Vacancy("Python Dev", 150000, "desc", "Moscow", "url")
    temp_handler.add_vacancy(vacancy)

    vacancies = temp_handler.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Python Dev"


def test_avoid_duplicate_vacancies(temp_handler: JSONFileHandler) -> None:
    """Проверка, что дубликаты не добавляются."""
    vacancy = Vacancy("Python Dev", 150000, "desc", "Moscow", "url")
    temp_handler.add_vacancy(vacancy)
    temp_handler.add_vacancy(vacancy)

    data = temp_handler.get_vacancies()
    assert len(data) == 1


def test_get_vacancies_by_criteria(temp_handler: JSONFileHandler) -> None:
    """Проверка фильтрации вакансий по критериям."""
    v1 = Vacancy("Backend", 120000, "desc", "SPB", "url1")
    v2 = Vacancy("Frontend", 100000, "desc", "Moscow", "url2")

    temp_handler.add_vacancy(v1)
    temp_handler.add_vacancy(v2)

    result = temp_handler.get_vacancies(city="SPB")
    assert len(result) == 1
    assert result[0]["title"] == "Backend"


def test_delete_vacancy(temp_handler: JSONFileHandler) -> None:
    """Проверка удаления вакансии по названию."""
    v1 = Vacancy("DevOps", 130000, "desc", "Kazan", "url")
    v2 = Vacancy("ML Engineer", 160000, "desc", "Kazan", "url")

    temp_handler.add_vacancy(v1)
    temp_handler.add_vacancy(v2)

    temp_handler.delete_vacancy("DevOps")
    remaining = temp_handler.get_vacancies()

    assert len(remaining) == 1
    assert remaining[0]["title"] == "ML Engineer"
