import random


class Cat:
    def __init__(self, name):
        self.name = name
        self.happiness = 50
        self.satiety = 50
        self.health = 100
        self.alive = True

    def to_eat(self):
        print("The cat is eating")
        self.satiety += 20
        self.happiness += 3

    def to_sleep(self):
        print("The cat is sleeping")
        self.health += 5
        self.satiety -= 5

    def to_play(self):
        print("The cat is playing")
        self.happiness += 10
        self.satiety -= 10

    def to_wash(self):
        print("The cat is washing itself")
        self.health += 2
        self.happiness += 2

    def is_alive(self):
        if self.satiety <= 0:
            print("The cat starved...")
            self.alive = False
        elif self.health <= 0:
            print("The cat got sick...")
            self.alive = False
        elif self.happiness <= 0:
            print("The cat is very unhappy...")
            self.alive = False

    def end_of_day(self):
        print(f"Happiness is {self.happiness}")
        print(f"Satiety is {self.satiety}")
        print(f"Health is {self.health}")

    def live(self, day):
        print(f"Day {day} of {self.name}'s life")

        live_cube = random.randint(1, 4)

        if live_cube == 1:
            self.to_eat()
        elif live_cube == 2:
            self.to_sleep()
        elif live_cube == 3:
            self.to_play()
        elif live_cube == 4:
            self.to_wash()

        self.end_of_day()
        self.is_alive()


cat = Cat(name="Murka")

for day in range(365):
    if not cat.alive:
        break
    cat.live(day)