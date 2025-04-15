from typing import List

import pytest

from src.utils import filter_by_keywords, get_top_vacancies, sort_by_salary
from src.vacancy import Vacancy


@pytest.fixture
def sample_vacancies() -> List[Vacancy]:
    """Создаёт набор тестовых вакансий."""
    return [
        Vacancy("Python Developer", 150000, "Backend and Django", "Moscow", "url1"),
        Vacancy("Frontend Developer", 120000, "React и Vue", "SPB", "url2"),
        Vacancy("DevOps Engineer", 180000, "CI/CD и облака", "Kazan", "url3"),
        Vacancy("Data Scientist", 170000, "ML, Python, AI", "Novosibirsk", "url4"),
    ]


def test_filter_by_keywords(sample_vacancies: List[Vacancy]) -> None:
    """Проверяет фильтрацию вакансий по ключевым словам."""
    result = filter_by_keywords(sample_vacancies, ["python", "react"])
    titles = [v.title for v in result]
    assert "Python Developer" in titles
    assert "Frontend Developer" in titles
    assert "Data Scientist" in titles
    assert "DevOps Engineer" not in titles


def test_sort_by_salary_desc(sample_vacancies: List[Vacancy]) -> None:
    """Проверяет сортировку по убыванию зарплаты."""
    sorted_vacancies = sort_by_salary(sample_vacancies)
    salaries = [v.salary for v in sorted_vacancies]
    assert salaries == sorted(salaries, reverse=True)


def test_sort_by_salary_asc(sample_vacancies: List[Vacancy]) -> None:
    """Проверяет сортировку по возрастанию зарплаты."""
    sorted_vacancies = sort_by_salary(sample_vacancies, if_reverse=False)
    salaries = [v.salary for v in sorted_vacancies]
    assert salaries == sorted(salaries)


def test_get_top_vacancies(sample_vacancies: List[Vacancy]) -> None:
    """Проверяет получение топ-N вакансий по зарплате."""
    top = get_top_vacancies(sample_vacancies, 2)
    assert len(top) == 2
    assert top[0].salary >= top[1].salary
