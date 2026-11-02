import random


brand_of_car = {
    "BMW": {"fuel": 100, "strength": 100, "consumption": 6},
    "Lada": {"fuel": 50, "strength": 40, "consumption": 10},
    "Volvo": {"fuel": 70, "strength": 150, "consumption": 8},
    "Ferrari": {"fuel": 80, "strength": 120, "consumption": 14}
}


job_list = {
    "Java developer": {"salary": 50, "gladness_less": 10},
    "Python developer": {"salary": 40, "gladness_less": 3},
    "C++ developer": {"salary": 45, "gladness_less": 25},
    "Rust developer": {"salary": 70, "gladness_less": 1}
}

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
        print(f"Играю с питомцем {self.pet.name}!")
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

        if self.is_alive() == False:
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
                print(
                    f"I get a job {self.job.job} "
                    f"with salary {self.job.salary}"
                )

        self.days_indexes(day)

        dice = random.randint(1, 5)


        if self.satiety < 20:
            print("I'll go eat")
            self.eat()

        elif self.gladness < 20:

            if self.home.mess > 15:
                print(
                    "I want to chill, but there is so much mess...\n"
                    "So I will clean the house"
                )
                self.clean_home()

            else:
                print("Let's chill!")
                self.chill()

        elif self.money < 0:
            print("Start working")
            self.work()

        elif self.car.strength < 15:
            print("I need to repair my car")
            self.to_repair()

        elif dice == 1:
            print("Let's chill!")
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

        elif dice == 5:
            print("Time to play with the pet!")
            self.play_with_pet()


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


test_human = Human(name="VLAD")


for day in range(1, 8):

    if test_human.live(day) == False:
        break