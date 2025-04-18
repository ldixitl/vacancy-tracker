import pytest

from src.vacancy import Vacancy


class MockConverter:
    """Заглушка конвертера валют, возвращает RUB в 100 раз больше переданной суммы."""

    def convert_to_rub(self, amount: int, currency: str) -> int:
        return amount * 100  # например: 1 USD = 100 RUB


@pytest.fixture(autouse=True)
def mock_converter(monkeypatch) -> None:
    """Фикстура для замены настоящего конвертера валют на заглушку."""
    monkeypatch.setattr(Vacancy, "_converter", MockConverter())


def test_vacancy_with_int_salary() -> None:
    """Проверяет корректную инициализацию вакансии с зарплатой в виде числа."""
    vac = Vacancy("Python Dev", 150000, "Some desc", "Moscow", "http://example.com")
    assert vac.salary == 150000
    assert vac.title == "Python Dev"
    assert vac.city == "Moscow"
    assert vac.url == "http://example.com"
    assert "Python Dev" in repr(vac)


def test_vacancy_with_dict_salary_avg() -> None:
    """Проверяет расчёт средней зарплаты при наличии 'from' и 'to' в словаре."""
    vac = Vacancy("Backend", {"from": 1000, "to": 2000, "currency": "USD"}, "Desc", "SPB", "url")
    assert vac.salary == 150000  # (1000+2000)//2 * 100


def test_vacancy_with_dict_salary_only_from() -> None:
    """Проверяет обработку зарплаты, если указан только 'from'."""
    vac = Vacancy("Frontend", {"from": 1200, "currency": "USD"}, "Desc", "Kazan", "url")
    assert vac.salary == 120000


def test_vacancy_with_dict_salary_only_to() -> None:
    """Проверяет обработку зарплаты, если указан только 'to'."""
    vac = Vacancy("Fullstack", {"to": 800, "currency": "USD"}, "Desc", "Omsk", "url")
    assert vac.salary == 80000


def test_vacancy_with_none_salary() -> None:
    """Проверяет корректную обработку случая, когда зарплата отсутствует."""
    vac = Vacancy("QA", None, "No desc", "", "")
    assert vac.salary == 0
    assert vac.title == "QA"
    assert vac.city == "Город не указан"
    assert vac.url == "Ссылка не указана"
    assert vac.description == "No desc"


def test_vacancy_comparison() -> None:
    """Проверяет сравнение вакансий по зарплате: <, >, ==."""
    vac1 = Vacancy("A", 100000, "desc", "city", "url")
    vac2 = Vacancy("B", 150000, "desc", "city", "url")
    assert vac1 < vac2
    assert vac2 > vac1
    assert vac1 != vac2

    vac3 = Vacancy("C", 100000, "desc", "city", "url")
    assert vac1 == vac3


def test_invalid_comparison() -> None:
    """Проверяет, что сравнение с не-Vacancy объектом вызывает TypeError."""
    vac = Vacancy("Dev", 100000, "desc", "city", "url")
    with pytest.raises(TypeError):
        vac < "not a vacancy"
    with pytest.raises(TypeError):
        vac > "not a vacancy"
    with pytest.raises(TypeError):
        vac == "not a vacancy"
