def safe_calculator_decorator(func):
  def wrapper(expression):
    try:
      # Выполняем ориджинал функшн
      result = func(expression)
      return result
    except ZeroDivisionError:
      return "Помилка: неможливо ділити на нуль!"
    except SyntaxError:
      return "Помилка: некоректний синтаксис виразу!"
    except Exception as e:
      return f"Сталася непередбачена помилка: {e}"

  return wrapper


@safe_calculator_decorator
def calculate(expression):
  return eval(expression)


# Проверка калькУлятора
print(calculate("2 + 2 * 2"))
print(calculate("10 / 0"))
print(calculate("2 + ( 3 "))