# Проект *Vacancy Tracker*

## Описание

*Vacancy Tracker* — это консольное приложение для поиска, фильтрации и анализа вакансий с платформы hh.ru. Программа позволяет получать вакансии через API, сохранять их в файл, фильтровать по ключевым словам, сортировать по зарплате и выбирать топ-вакансии.

### Реализованные функции:
#### Взаимодействие с API (модуль `external_api.py`)
- **Получение вакансий с hh.ru** (`HeadHunterAPI`) — получает вакансии по заданному ключевому слову с постраничной загрузкой и отображением прогресса.
- **Форматирование вакансий** — преобразует данные с API в удобный формат.

#### Обработка и представление вакансий (модуль `vacancy.py`)
- **Модель вакансии** (`Vacancy`) — объект с полями `title`, `salary`, `description`, `city`, `url`, с валидацией, свойствами и магическими методами сравнения.
- **Конвертация валют** — с помощью класса `CurrencyConverter`, вакансии автоматически переводятся в рубли на основе курсов ЦБ РФ.

#### Работа с файлами (модуль `file_handlers.py`)
- **Интерфейс для хранения вакансий** (`FileHandler`) — абстрактный класс.
- **Хранение вакансий в JSON** (`JSONFileHandler`) — реализация хранения и удаления вакансий по названию.

#### Утилиты (модуль `utils.py`)
- **Фильтрация вакансий** (`filter_by_keywords`) — отбор вакансий по ключевым словам.
- **Сортировка по зарплате** (`sort_by_salary`) — по убыванию или возрастанию.
- **Выборка топ-N вакансий** (`get_top_vacancies`) — возвращает лучшие предложения.

#### Обработка валют (модуль `currency.py`)
- **Получение курсов валют** (`CurrencyConverter`) — загружает данные с сайта ЦБ РФ.
- **Конвертация в рубли** (`convert_to_rub`) — обрабатывает зарплаты, заданные в иностранных валютах.

#### Абстрактные классы (модуль `base.py`)
- **VacancyAPI** — абстрактный класс для работы с API платформ вакансий. Определяет методы `_connect()` и `get_vacancies()`.
- **FileHandler** — абстрактный интерфейс для хранения и обработки вакансий. Определяет методы `add_vacancy()`, `get_vacancies()`, `delete_vacancy()`.

## Примеры работы функций

### Получение и фильтрация вакансий по ключевым словам
```python
from src.external_api import HeadHunterAPI
from src.utils import filter_by_keywords

api = HeadHunterAPI()
vacancies = api.get_vacancies("python разработчик")
filtered = filter_by_keywords(vacancies, ["django", "flask"])
print(filtered)
```

### Сортировка вакансий по зарплате
```python
from src.utils import sort_by_salary
from src.vacancy import Vacancy

vacancies = [
    Vacancy("Backend", 120000, "desc", "Moscow", "url"),
    Vacancy("DevOps", 180000, "desc", "SPB", "url"),
]
sorted_vacancies = sort_by_salary(vacancies)
print(sorted_vacancies)
```

### Получение топ-N вакансий
```python
from src.utils import get_top_vacancies

top_3 = get_top_vacancies(vacancies, 3)
for vacancy in top_3:
    print(vacancy)
```

### Конвертация валют в рубли
```python
from src.currency import CurrencyConverter

converter = CurrencyConverter()
print(converter.convert_to_rub(1000, "USD"))
```

### Сохранение и удаление вакансий
```python
from src.file_handlers import JSONFileHandler
from src.vacancy import Vacancy

handler = JSONFileHandler("vacancies.json")
vac = Vacancy("ML Engineer", 150000, "desc", "Kazan", "url")
handler.add_vacancy(vac)
handler.delete_vacancy("ML Engineer")
```

## Установка
1. Клонируйте репозиторий:
```sh
git clone https://github.com/ldixitl/vacancy-tracker.git
```
Используется Poetry для управления зависимостями. Убедитесь, что Poetry установлен.
После установки выполните:
2. Установите зависимости:
```sh
poetry install
```

## Использование
Запуск основного скрипта:
```sh
python main.py
```
Приложение загружает вакансии, позволяет их отфильтровать, отсортировать и сохранить в файл.

## Тестирование
Для тестирования в проекте используются **pytest** и плагин **pytest-cov** для измерения покрытия кода тестами.

### Запуск тестов
Чтобы запустить тесты, выполните команду:
```bash
pytest
```

### Отчёт о покрытии кода
Для генерации отчёта о покрытии кода в формате HTML выполните:

```bash
pytest --cov=src --cov-report=html
```
После выполнения команда сгенерирует папку **htmlcov**, содержащую отчёт. 
Откройте файл **htmlcov/index.html** в браузере, чтобы просмотреть детализированный отчёт.

## Лицензия
Этот проект лицензирован по [лицензии MIT](LICENSE).
