import time

from tqdm import tqdm

from src.external_api import HeadHunterAPI
from src.file_handlers import JSONFileHandler
from src.utils import filter_by_keywords, get_top_vacancies
from src.vacancy import Vacancy


def main() -> None:
    """Главная функция, запускающая все реализованные модули проекта."""
    print("🔎 Добро пожаловать в Поиск вакансий!\n")
    time.sleep(0.5)

    search_query = input("Введите профессию, должность или компанию (например: Python-разработчик): \n").strip()
    api = HeadHunterAPI()
    vacancies_data = api.get_vacancies(search_query)

    # Преобразование данных в объекты Vacancy
    vacancy_list = []
    print("📦 Обработка вакансий...")
    for item in tqdm(vacancies_data, desc="Загрузка данных"):
        vacancy = Vacancy(
            title=item.get("name"),
            salary=item.get("salary"),
            description=item.get("description"),
            city=item.get("area", {}).get("name"),
            url=item.get("alternate_url"),
        )
        vacancy_list.append(vacancy)

    if not vacancy_list:
        print("⚠️ Вакансии не найдены.")
        return

    print(f"\n✅ Найдено вакансий: {len(vacancy_list)}")

    # Сохранение вакансий в файл
    save_choice = input("💾 Хотите сохранить вакансии в файл? (y/n): ").strip().lower()

    if save_choice == "y":
        filename = input("Введите название файла (Enter — по умолчанию 'vacancies.json'): ").strip()
        file_handler = JSONFileHandler(filename) if filename else JSONFileHandler()

        print("📁 Сохранение вакансий в папку 'data'...")
        for vac in tqdm(vacancy_list, desc="Сохранение"):
            file_handler.add_vacancy(vac)

        print("✅ Сохранение завершено. Вакансии сохранены в папке 'data'.")
    else:
        print("⚠️ Сохранение отменено.")

    while True:
        time.sleep(0.5)
        print("\nВыберите действие:")
        print("1 - Показать топ-N вакансий по зарплате")
        print("2 - Фильтровать по ключевым словам")
        print("3 - Показать все вакансии")
        print("0 - Выход")

        time.sleep(0.5)
        user_choice = input("Введите номер действия: ").strip()

        if user_choice == "1":
            try:
                n = int(input("Введите количество вакансий для вывода: "))
                top_vacancies = get_top_vacancies(vacancy_list, n)
                for vac in top_vacancies:
                    print(f"➢ {vac}")

            except ValueError:
                print("⚠️ Введите целое число.")

        elif user_choice == "2":
            keywords = input("Введите ключевые слова через пробел: ").split()
            filtered = filter_by_keywords(vacancy_list, keywords)
            if filtered:
                for vac in filtered:
                    print(f"➢ {vac}")
            else:
                print("️⚠️ Вакансии с такими ключевыми словами не найдены.")

        elif user_choice == "3":
            for vac in vacancy_list:
                print(f"➢ {vac}")

        elif user_choice == "0":
            print("👋🏻 Выход из программы.")
            time.sleep(0.5)
            break

        else:
            print("⚠️ Неверный выбор. Повторите.")


if __name__ == "__main__":
    main()
