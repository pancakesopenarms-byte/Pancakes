from datetime import datetime
import sqlite3
import time
from bs4 import BeautifulSoup
import requests

DB_NAME = "weather.db"
URL = "https://sinoptik.ua/pohoda/chernihiv"
INTERVAL_SECONDS = 30 * 60  # 30 минут = 1800 секунд


def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recorded_at TEXT NOT NULL,
            temperature TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def get_chernihiv_temperature(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    temp_el = soup.find(class_=lambda c: c and "today-temp" in c)
    if temp_el and temp_el.get_text(strip=True):
        return temp_el.get_text(strip=True)

    for tag in soup.find_all(["p", "span", "div"]):
        text = tag.get_text(strip=True)
        if "°" in text and len(text) <= 6 and any(ch.isdigit() for ch in text):
            return text

    raise ValueError("Не удалось найти температуру на странице")


def save_weather(conn: sqlite3.Connection, recorded_at: str, temperature: str) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO weather (recorded_at, temperature) VALUES (?, ?)",
        (recorded_at, temperature),
    )
    conn.commit()


def run_monitoring() -> None:
    conn = init_db(DB_NAME)
    print(f"Мониторинг запущен. Интервал: {INTERVAL_SECONDS // 60} мин. Для выхода нажми Ctrl+C / Stop.")

    try:
        while True:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                temp = get_chernihiv_temperature(URL)
                save_weather(conn, now_str, temp)
                print(f"[{now_str}] Записано в БД: {temp}")
            except Exception as exc:
                print(f"[{now_str}] Ошибка при обновлении погоды: {exc}")

            # Ждём 30 минут
            for _ in range(INTERVAL_SECONDS):
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nСканирование остановлено пользователем.")
    finally:
        conn.close()
        print("Соединение с БД закрыто.")


if __name__ == "__main__":
    run_monitoring()