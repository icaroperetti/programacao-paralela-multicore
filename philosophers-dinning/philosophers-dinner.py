import random
import time
from threading import Thread, Lock
from colorama import Fore

meals_eated = [0, 0, 0, 0, 0]


class Philosofer(Thread):
    running = True

    def __init__(self, name, left_fork, right_fork):
        Thread.__init__(self)
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.name = name
        self.time_eating = random.randint(1, 5)  # Time eating
        self.time_without_eating = random.uniform(
            15, 20)  # Time max without eating

    def run(self):
        while self.running:
            time_waiting = 0
            random_time = random.randint(5, 15)

            print(Fore.BLUE + f"{self.name} is thinking")
            time.sleep(random_time)

            eated = self.eat()

            # Check if the philosopher has eaten
            if eated == True:
                time_waiting = 0
            else:
                time_waiting += random_time

            # Starvation
            # Check if the philosopher has been waiting for more than the time he can wait, if so, he eats
            if (time_waiting + 4) > self.time_without_eating:
                # self.running = False
                # print(f"{self.name} died of hunger")
                self.left_fork.acquire(True)
                self.right_fork.acquire(True)
                print(Fore.GREEN + f"{self.name} started eating (STARVATION)")
                time.sleep(self.time_eating)

                print(Fore.GREEN + f"{self.name} finished eating")
                # Release the forks so the other philosophers can eat
                self.left_fork.release()
                self.right_fork.release()

    def eat(self):
        first_fork, second_fork, name = self.left_fork, self.right_fork, self.name
        print(Fore.YELLOW + f"{name} trying to get a fork")

        if first_fork.acquire(False):  # Check if the first fork is not being used
            print(Fore.WHITE + f"{name} got the first fork")

            # Check if the second fork is not being used
            if second_fork.acquire(False):
                print(Fore.WHITE + f"{name} got the second fork")

                print(Fore.RED + f"{name} is eating\n")
                time.sleep(self.time_eating)
                meals_eated[names.index(self.name)] += 1
                print(Fore.BLACK + f"{name} finished eating\n")

                print(Fore.GREEN +
                      f"Each Philosopher has eaten: {meals_eated}", )

                first_fork.release()
                second_fork.release()

                return True
            # If the second fork is being used, release the first fork
            else:
                # print(f"{name} couldn't get another chopstick")
                first_fork.release()
                return False


names = ['Aristoteles', 'Platão', 'Kant', 'Descartes', 'Sócrates']
forks = [Lock() for _ in range(5)]
table = [Philosofer(names[i], forks[i], forks[(i+1) % 5]) for i in range(5)]

for filosofo in table:
    filosofo.start()
    time.sleep(0.8)
