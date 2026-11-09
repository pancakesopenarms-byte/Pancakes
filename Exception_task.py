result = []

def divider(a, b):
    if a < b:
        raise ValueError("Значення 'a' менше за 'b'")
    if b > 100:
        raise IndexError("Значення 'b' перевищує 100")
    return a / b

data = {10: 2, 2: 5, "123": 4, 18: 0, "list_placeholder": 15, 8: 4}

for key in data:
    try:
        # Исправляем опечатку: data[kem] заменено на data[key]
        res = divider(key, data[key])
        result.append(res)
    except Exception as e:
        print(f"Помилка для ключа '{key}': {type(e).__name__} - {e}")

print("\Результат успішних обчислень:")
print(result)