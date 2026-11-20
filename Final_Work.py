import random
import sqlite3


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


#БАЗА ДАННЫХ
class GameDatabase:

  def __init__(self):
    self.connection = sqlite3.connect("game_stats.db")
    self.cursor = self.connection.cursor()

    self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                game_name TEXT PRIMARY KEY,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0
            )
        """)

    # Очистка базы данных при каждом новом запуске,потому что так надо.
    self.cursor.execute("DELETE FROM games")
    self.connection.commit()

    self.session_stats = {
        "Guess the number": {"wins": 0, "losses": 0},
        "Coin flip": {"wins": 0, "losses": 0},
        "Rock Paper Scissors": {"wins": 0, "losses": 0},
    }

  def add_result(self, game_name, won):
    if won:
      self.session_stats[game_name]["wins"] += 1
    else:
      self.session_stats[game_name]["losses"] += 1

    self.cursor.execute(
        """
            INSERT INTO games (game_name, wins, losses)
            VALUES (?, ?, ?)
            ON CONFLICT(game_name) DO UPDATE SET
            wins = wins + excluded.wins,
            losses = losses + excluded.losses
        """,
        (game_name, int(won), int(not won)),
    )
    self.connection.commit()

  def show_stats(self):
    self.cursor.execute("SELECT * FROM games")
    results = self.cursor.fetchall()

  def show_session_stats(self):
    print("\n========== CURRENT SESSION ==========")
    total_wins = 0
    total_losses = 0

    for game, stats in self.session_stats.items():
      wins = stats["wins"]
      losses = stats["losses"]
      total_wins += wins
      total_losses += losses

      print(f"\nGame: {game}")
      print(f"Wins: {wins}")
      print(f"Losses: {losses}")
      print(f"Total: {wins + losses}")

    print("----------------------------------------")
    print(f"Total wins: {total_wins}")
    print(f"Total losses: {total_losses}")
    print(f"Total games: {total_wins + total_losses}")
    print("========================================")

  def close(self):
    self.connection.close()


database = GameDatabase()


class Pet:

  def __init__(self, name="Frosya"):
    self.name = name
    self.gladness = 50
    self.satiety = 50

  def eat(self):
    self.satiety += 10
    if self.satiety > 100:
      self.satiety = 100

  def play(self):
    self.gladness += 15
    self.satiety -= 5


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

  def get_home(self):
    self.home = House()

  def get_pet(self):
    self.pet = Pet("Frosya")

  def get_car(self):
    self.car = Auto(brand_of_car)

  def get_job(self):
    if self.car.drive():
      self.job = Job(job_list)
    else:
      if self.car.fuel < self.car.consumption:
        self.shopping("fuel")
      else:
        self.to_repair()

  # МИНИ-ИГРЫ
  def play_minigame(self):
    game_number = random.randint(1, 3)
    print("\n========== MINI GAME ==========")

    if game_number == 1:
      game_name = "Guess the number"
      print("Guess a number from 1 to 3!")
      number = random.randint(1, 3)
      try:
        answer = int(input("Your answer: "))
        won = answer == number
      except ValueError:
        print("Invalid input!")
        won = False
      print(f"The correct number was: {number}")

    elif game_number == 2:
      game_name = "Coin flip"
      print("GAME: Heads or tails!")
      coin = random.choice(["heads", "tails"])
      answer = input("Choose heads or tails: ").lower().strip()# методы:нижний регистр и убиратель пробелов
      print(f"The coin landed on: {coin}")
      won = answer == coin

    else:
      game_name = "Rock Paper Scissors"
      print("Rock, Paper or Scissors!")
      choices = ["rock", "paper", "scissors"]
      computer = random.choice(choices)
      answer = input("Your choice: ").lower().strip() # та же дичб
      print(f"Computer chose: {computer}")

      if answer not in choices:
        won = False
      elif answer == computer:
        print("Draw! This counts as a loss.")
        won = False
      elif (
          (answer == "rock" and computer == "scissors")
          or (answer == "paper" and computer == "rock")
          or (answer == "scissors" and computer == "paper")
      ):
        won = True
      else:
        won = False

    if won:
      print("\n========== YOU WON! ==========")
    else:
      print("\n========== YOU LOST! ==========")

    database.add_result(game_name, won)
    input("\nPress ENTER to continue...")
    return won

  def perform_action(self, action):
    print("\nRolling the game dice...")
    dice = random.randint(1, 6)
    print(f"Dice result: {dice}")

    if dice <= 2:
      print("A MINI GAME HAS STARTED!")
      if not self.play_minigame():
        print("Action cancelled due to loss!")
        return

    print("Action successfully performed!")
    action()

  def eat(self):
    if self.home.food <= 0:
      self.shopping("food")
    else:
      if self.satiety >= 100:
        self.satiety = 100
        return
      self.satiety += 5
      self.home.food -= 5

  def work(self):
    if not self.car.drive():
      if self.car.fuel < self.car.consumption:
        self.shopping("fuel")
      else:
        self.to_repair()
      return

    self.money += self.job.salary
    self.gladness -= self.job.gladness_less
    self.satiety -= 4

  def shopping(self, manage):
    if manage == "fuel":
      print("I bought fuel")
      self.money -= 100
      self.car.fuel += 100
      return

    if not self.car.drive():
      if self.car.fuel < self.car.consumption:
        print("The car has no fuel")
        self.money -= 100
        self.car.fuel += 100
      else:
        self.to_repair()
      return

    if manage == "food":
      print("Bought food")
      self.money -= 50
      self.home.food += 50
    elif manage == "delicacies":
      print("Hooray! Delicious!")
      self.gladness += 10
      self.satiety += 2
      self.money -= 15

  def chill(self):
    self.gladness += 10
    self.home.mess += 5

  def play_with_pet(self):
    print(f"Playing with pet {self.pet.name}!")
    self.pet.play()
    self.gladness += 10
    self.satiety -= 5

  def clean_home(self):
    self.gladness -= 5
    self.home.mess = 0

  def to_repair(self):
    self.car.strength += 100
    self.money -= 50

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
      print("Depression...")
      return False
    if self.satiety < 0:
      print("Dead...")
      return False
    if self.money < -500:
      print("Bankrupt...")
      return False
    return True

  def live(self, day):
    if not self.is_alive():
      return False

    if self.home is None:
      print("Settled in the house")
      self.get_home()

    if self.pet is None:
      self.get_pet()
      print(f"I got a pet named {self.pet.name}")

    if self.car is None:
      self.get_car()
      print(f"I bought a car {self.car.brand}")

    if self.job is None:
      self.get_job()
      if self.job is not None:
        print(f"I got a job {self.job.job} with salary {self.job.salary}")

    self.days_indexes(day)
    dice = random.randint(1, 5)

    if self.satiety < 20:
      print("I'll go eat")
      self.eat()
    elif self.gladness < 20:
      if self.home.mess > 15:
        print("I need to clean the house")
        self.perform_action(self.clean_home)
      else:
        print("Let's chill!")
        self.perform_action(self.chill)
    elif self.money < 0:
      print("Start working")
      self.perform_action(self.work)
    elif self.car.strength < 15:
      print("I need to repair my car")
      self.to_repair()
    elif dice == 1:
      print("Let's chill!")
      self.perform_action(self.chill)
    elif dice == 2:
      print("Start working")
      self.perform_action(self.work)
    elif dice == 3:
      print("Cleaning time!")
      self.perform_action(self.clean_home)
    elif dice == 4:
      print("Time for treats!")
      self.perform_action(lambda: self.shopping("delicacies"))
    elif dice == 5:
      print("Time to play with the pet!")
      self.perform_action(self.play_with_pet)


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
      print("The car cannot move")
      return False


class House:

  def __init__(self):
    self.mess = 0
    self.food = 0


class Job:

  def __init__(self, job_list):
    self.job = random.choice(list(job_list))
    self.salary = job_list[self.job]["salary"]
    self.gladness_less = job_list[self.job]["gladness_less"]


# ЗАПУСК
test_human = Human(name="VLAD")

try:
  for day in range(1, 8):
    if test_human.live(day) == False:
      break

  print("\n========== FINAL RESULTS ==========")
  database.show_session_stats()
  database.show_stats()

finally:
  database.close()