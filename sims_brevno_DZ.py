import functools
import logging
import random
import time


logging.basicConfig(
    filename="simulation.log",
    filemode="w",  # очистка симулятора
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

# Вывод бревен
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)


# Декоратор для замера времени
def time_tracker(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    start_time = time.time()  # Засекаем начало
    result = func(*args, **kwargs)  # Выполняем
    end_time = time.time()  # Засекаем финал
    execution_time = end_time - start_time

    message = f"Функція '{func.__name__}' виконувалася: {execution_time:.4f} секунд."
    print(f"\n[TIME TRACKER] {message}")
    logging.info(message)

    return result

  return wrapper


brand_of_car = {
    "BMW": {"fuel": 100, "strength": 100, "consumption": 6},
    "Lada": {"fuel": 50, "strength": 40, "consumption": 10},
    "Volvo": {"fuel": 70, "strength": 150, "consumption": 8},
    "Ferrari": {"fuel": 80, "strength": 120, "consumption": 14},
}
job_list = {
    "Java developer": {"salary": 50, "gladness_less": 10},
    "Python developer": {"salary": 40, "gladness_less": 3},
    "C++ developer": {"salary": 45, "gladness_less": 25},
    "Rust developer": {"salary": 70, "gladness_less": 1},
}


class Pet:

  def __init__(self, name="Barsik"):
    self.name = name
    self.gladness = 50
    self.satiety = 50

  def eat(self):
    self.satiety += 10
    if self.satiety > 100:
      self.satiety = 100
    logging.info(f"Pet {self.name} ate. Satiety: {self.satiety}")

  def play(self):
    self.gladness += 15
    self.satiety -= 5
    logging.info(f"Pet {self.name} played. Gladness: {self.gladness}")


class Human:

  def __init__(self, name="Human", job=None, home=None, car=None, pet=None):
    self.name = name
    self.money = 100
    self.gladness = 50
    self.satiety = 50
    self.job = job
    self.home = home
    self.car = car
    self.pet = pet
    logging.info(f"Human {self.name} was born with {self.money} money.")

  def get_home(self):
    self.home = House()
    logging.info(f"{self.name} settled in the house.")

  def get_pet(self):
    self.pet = Pet("Barsik")
    logging.info(f"{self.name} got a pet.")

  def get_car(self):
    self.car = Auto(brand_of_car)
    logging.info(f"{self.name} bought a car: {self.car.brand}.")

  def get_job(self):
    if self.car.drive():
      pass
    else:
      logging.warning(
          f"{self.name} couldn't drive to get a job. Car needs repair."
      )
      self.to_repair()
      return
    self.job = Job(job_list)
    logging.info(
        f"{self.name} got a job as {self.job.job} with salary"
        f" {self.job.salary}."
    )

  def eat(self):
    if self.home.food <= 0:
      logging.warning(f"{self.name} has no food at home. Going shopping.")
      self.shopping("food")
    else:
      if self.satiety >= 100:
        self.satiety = 100
        return
      self.satiety += 5
      self.home.food -= 5
      logging.info(f"{self.name} ate. Satiety: {self.satiety}")

  def work(self):
    if self.car.drive():
      pass
    else:
      if self.car.fuel < 20:
        logging.warning(f"{self.name}'s car is low on fuel. Going for fuel.")
        self.shopping("fuel")
        return
      else:
        logging.warning(f"{self.name}'s car broke down. Going to repair.")
        self.to_repair()
        return
    self.money += self.job.salary
    self.gladness -= self.job.gladness_less
    self.satiety -= 4
    logging.info(
        f"{self.name} worked. Earned {self.job.salary}. Money: {self.money}"
    )

  def shopping(self, manage):
    if self.car.drive():
      pass
    else:
      if self.car.fuel < 20:
        logging.warning(
            f"{self.name} needs fuel during shopping trip. Buying fuel."
        )
        self.shopping("fuel")
        return
      else:
        logging.warning(f"{self.name} car broken during shopping. Repairing.")
        self.to_repair()
        return
    if manage == "food":
      logging.info(f"{self.name} bought food.")
      self.money -= 50
      self.home.food += 50
    elif manage == "fuel":
      logging.info(f"{self.name} bought fuel.")
      self.money -= 100
      self.car.fuel += 100
    elif manage == "delicacies":
      logging.info(f"{self.name} bought delicacies.")
      self.gladness += 10
      self.satiety += 2
      self.money -= 15

  def chill(self):
    self.gladness += 10
    self.home.mess += 5
    logging.info(f"{self.name} is chilling. Gladness: {self.gladness}")

  def play_with_pet(self):
    logging.info(f"{self.name} plays with pet.")
    self.pet.play()

  def clean_home(self):
    self.gladness -= 5
    self.home.mess = 0
    logging.info(f"{self.name} cleaned the house. Mess is 0.")

  def to_repair(self):
    self.car.strength += 100
    self.money -= 50
    logging.info(f"{self.name} repaired the car. Money left: {self.money}")

  def days_indexes(self, day):
    mes1 = f"Today the {day} of {self.name}'s life"
    print(f"{mes1:=^50}", "\n")
    h_index = self.name + "'s indexes"
    print(f"{h_index:-^50}", "\n")
    print(f"Money - {self.money}")
    print(f"Satiety - {self.satiety}")
    print(f"Gladness - {self.gladness}")
    mes2 = "Home indexes"
    print(f"{mes2:-^50}", "\n")
    print(f"Food - {self.home.food}")
    print(f"Mess - {self.home.mess}")
    mes3 = f"{self.car.brand} car indexes"
    print(f"{mes3:-^50}", "\n")
    print(f"Fuel - {self.car.fuel}")
    print(f"Strength - {self.car.strength}")

  def is_alive(self):
    if self.gladness < 0:
      logging.error(f"{self.name} fell into depression. Game over.")
      print("Depression...")
      return False
    if self.satiety < 0:
      logging.error(f"{self.name} died of hunger. Game over.")
      print("Dead...")
      return False
    if self.money < -500:
      logging.error(f"{self.name} went bankrupt. Game over.")
      print("Bankrupt...")
      return False

  def live(self, day):
    if self.is_alive() == False:
      return False
    if self.home is None:
      self.get_home()
    if self.car is None:
      self.get_car()
    if self.job is None:
      self.get_job()
    self.days_indexes(day)
    dice = random.randint(1, 4)
    if self.satiety < 20:
      print("I'll go eat")
      self.eat()
    elif self.gladness < 20:
      if self.home.mess > 15:
        print(
            "I want to chill, but there is so much mess…\n So I will clean the"
            " house"
        )
        self.clean_home()
      else:
        print("Let`s chill!")
        self.chill()
    elif self.money < 0:
      print("Start working")
      self.work()
    elif self.car.strength < 15:
      print("I need to repair my car")
      self.to_repair()
    elif dice == 1:
      print("Let`s chill!")
      self.chill()
    elif dice == 2:
      print("Start working")
      self.work()
    elif dice == 3:
      print("Cleaning time!")
      self.clean_home()
    elif dice == 4:
      print("Time for treats!")
      self.shopping(manage="delicacies")


class Auto:

  def __init__(self, brand_list):
    self.brand = random.choice(list(brand_list))
    self.fuel = brand_list[self.brand]["fuel"]
    self.strength = brand_list[self.brand]["strength"]
    self.consumption = brand_list[self.brand]["consumption"]

  def drive(self):
    if self.strength > 0 and self.fuel >= self.consumption:
      self.fuel -= self.consumption
      self.strength -= 1
      return True
    else:
      logging.warning(
          f"Car {self.brand} cannot move. Fuel: {self.fuel},"
          f" Strength: {self.strength}"
      )
      print("The car cannot move")
      return False


class House:

  def __init__(self, mess=0, food=0):
    self.mess = mess
    self.food = food


class Job:

  def __init__(self, job_list):
    self.job = random.choice(list(job_list))
    self.salary = job_list[self.job]["salary"]
    self.gladness_less = job_list[self.job]["gladness_less"]


# декор таймер
@time_tracker
def run_simulation():
  test_human = Human(name="Vasya")
  for day in range(1, 8):
    if test_human.live(day) == False:
      break


if __name__ == "__main__":
  run_simulation()