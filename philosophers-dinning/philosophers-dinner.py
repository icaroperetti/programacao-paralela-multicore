import random
import time
from colorama import Fore
from threading import Thread, Lock


class Philosofer(Thread):
    running = True

    def __init__(self, name, left_fork, right_fork):
        Thread.__init__(self)
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.name = name
        self.time_eating = random.randint(1, 5)  # Time eating
        self.time_without_eating = random.uniform(
            7, 12)  # Time max without eating

    def run(self):
        while self.running:
            time_waiting = 0
            random_time = random.uniform(5, 15)

            print(Fore.BLUE + f"{self.name} is thinking")
            time.sleep(random_time)

            eated = self.eat()

            # Check if the philosopher has eaten
            if eated == True:
                time_waiting = 0
            else:
                # If the philosopher didn't eat, add the time he was thinking to the time he is waiting
                time_waiting += random_time

            # Starvation resolution
            # Check if the philosopher has been waiting for more than the time he can wait, if so, he eats
            if (time_waiting + 2.5) > self.time_without_eating:
                # self.running = False
                # print(f"{self.name} died of hunger")
                self.left_fork.acquire(True)
                self.right_fork.acquire(True)
                print(Fore.GREEN + f"{self.name} started eating (STARVATION)")
                time.sleep(self.time_eating)

                print(Fore.RED + f"{self.name} finished eating")

                self.left_fork.release()
                self.right_fork.release()

    def eat(self):
        first_fork, second_fork, name = self.left_fork, self.right_fork, self.name
        print(f"{name} is hungry and tried to get a chopstick")
        if first_fork.acquire(False):  # Check if the first fork is not being used
            # print(f"{name} got a chopstick")

            # Check if the second fork is not being used
            if second_fork.acquire(False):
                # print(f"{name} got another chopstick")

                print(f"{name} is eating\n")
                time.sleep(self.time_eating)
                print(Fore.BLACK + f"{name} finished eating\n")

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
    time.sleep(1)
