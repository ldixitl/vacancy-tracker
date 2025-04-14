import requests


class CurrencyConverter:
    """Класс для загрузки курсов валют и конвертации в рубли."""

    _rates: dict = {}

    def __init__(self) -> None:
        """Загружает актуальные курсы валют при инициализации объекта конвертера."""
        self.load_rates()

    @classmethod
    def load_rates(cls) -> None:
        """Метод для загрузки актуальных курсов валют с сайта ЦБ РФ."""
        url = "https://www.cbr-xml-daily.ru/latest.js"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            cls._rates = data.get("rates", {})
        except (requests.RequestException, ValueError):
            print("Ошибка загрузки курсов валют. Конвертация невозможна.")
            cls._rates = {}

    def convert_to_rub(self, amount: int, currency: str) -> int:
        """
        Метод для конвертации суммы в рубли.

        :param amount: Сумма.
        :param currency: Валюта (например, 'USD').
        :return: Сумма в рублях (округлённая до int).
        """
        if currency == "RUR" or currency == "RUB" or not currency:
            return amount
        rate = self._rates.get(currency)
        if rate:
            return round(amount / rate)
        return 0
