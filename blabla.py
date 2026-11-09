import colorama
from colorama import Fore, Back, Style, init, AnsiToWin32
import inspect

print("=" * 60)
print("ЧАСТЬ 1: ИНТРОСПЕКЦІЯ БІБЛІОТЕКИ COLORAMA")
print("=" * 60)

# Чекаем модуль colorama через dir()
print(f"Все доступные объекты на уровне пакета colorama:\n{dir(colorama)}\n")

# Собираем главные компоненты для аналитики
components = {
    "Fore (Цвета текста)": Fore,
    "Back (Цвета фона)": Back,
    "Style (Стили текста)": Style,
    "init (Функция инициализации)": init,
    "AnsiToWin32 (Конвертер для Windows)": AnsiToWin32
}

for name, obj in components.items():
    print(f"--- Анализ элемента: {name} ---")
    print(f"Тип: {type(obj)}")

    # Очищаем список от служебной атрибутики
    public_attrs = [attr for attr in dir(obj) if not attr.startswith('_')]
    print(f"Публичные атрибуты: {public_attrs}\n")

print("=" * 60)
print("ЧАСТЬ 2: ДЕТАЛЬНЫЙ АНАЛИЗ ФУНКЦИИ init")
print("=" * 60)

# Используем модуль inspect, чтобы узнать параметры init
print(f"Сигнатура init(): {inspect.signature(init)}")
print(f"Документация (docstring) функции init:\n{inspect.getdoc(init)}\n")

print("=" * 60)
print("ЧАСТЬ 3: ДЕМОНСТРАЦИЯ РАБОТЫ (ПРИМЕРЫ)")
print("=" * 60)

# Инициализируем библиотеку (autoreset=True автоматически сбрасывает цвет после каждой строки)
init(autoreset=True)

print(Fore.RED + "Этот текст выведен красным цветом.")
print(Back.YELLOW + Fore.BLACK + "Текст с черными буквами на желтом фоне.")
print(Style.BRIGHT + "Этот текст сделан жирным.")
print("Этот текст снова стандартный, так как сработал autoreset=True.")