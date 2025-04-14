from typing import List

from vacancy import Vacancy


def filter_by_keywords(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """
    Фильтрует список вакансий по наличию ключевых слов в названии или описании.

    :param vacancies: Список вакансий.
    :param keywords: Ключевые слова для поиска.
    :return: Список вакансий, содержащих хотя бы одно ключевое слово.
    """
    keywords_lower = [keyword.lower() for keyword in keywords]

    result = []

    for vacancy in vacancies:
        combined_text = f"{vacancy.title} {vacancy.description}".lower()
        if any(keyword in combined_text for keyword in keywords_lower):
            result.append(vacancy)

    return result


def sort_by_salary(vacancies: List[Vacancy], if_reverse: bool = True) -> List[Vacancy]:
    """
    Сортирует вакансии по зарплате.

    :param vacancies: Список вакансий.
    :param if_reverse: True — по убыванию, False — по возрастанию.
    :return: Отсортированный список вакансий.
    """
    return sorted(vacancies, key=lambda x: x.salary, reverse=if_reverse)


def get_top_vacancies(vacancies: List[Vacancy], n: int) -> List[Vacancy]:
    """
    Возвращает топ-N вакансий из списка.

    :param vacancies: Список вакансий.
    :param n: Количество вакансий для возврата.
    :return: Список из n вакансий.
    """
    top_vacancy_by_salary = sort_by_salary(vacancies)
    return top_vacancy_by_salary[:n]
