import requests
from bs4 import BeautifulSoup


class CurrencyConverter:
    def __init__(self, usd_rate):
        self.usd_rate = usd_rate

    def uah_to_usd(self, uah_amount):
        return uah_amount / self.usd_rate


def get_usd_rate():
    # Ссылка на страницу официального курса валют НБУ
    url = "https://bank.gov.ua/ua/markets/exchangerates"

    # Отправляем запрос к сайту что бы не блокал
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # проверка на ошибки

    soup = BeautifulSoup(response.text, "html.parser")

    # Ищем все строки таблицы с курсами валют
    rows = soup.find_all("tr")
    for row in rows:
        if "USD" in row.text:
            cells = row.find_all("td")
            rate_text = cells[-1].text.strip().replace(",", ".")
            return float(rate_text)

    raise ValueError("Не удалось найти курс USD на странице")


#Основная часть
if __name__ == "__main__":
    try:
        current_rate = get_usd_rate()
        print(f"Актуальный курс НБУ: 1 USD = {current_rate} UAH")

        converter = CurrencyConverter(current_rate)

        # 3. Запрашиваем сумму деняк
        uah = float(input("Введите сумму в гривнах (UAH): "))
        usd = converter.uah_to_usd(uah)

        # Выводим результатs
        print(f"Сумма в долларах США: {usd:.2f} USD")

    except Exception as e:
        print(f"Произошла ошибка: {e}")