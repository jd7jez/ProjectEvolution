import pygame
import time
from Sun import Sun
from Plant import Plant
import random
import matplotlib.pyplot as plt
import sys

class Environment:
    def __init__(self, width=1400, height=900):
        self.WIDTH = width
        self.HEIGHT = height
        # Old ECR: 0.25-3.0
        # OLD SCR: 0.5-2.0
        self.BACKGROUND = (255, 255, 255)
        self.sun = Sun(self.WIDTH, self.HEIGHT, self.WIDTH, 10)
        self.plants = [Plant(random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT), 50.0, 0,
                             energy_change_rate=(random.random() *4.75) + 0.25, size_change_rate=(random.random() * 3.5) + 0.5)
                       for _ in range(50)]

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Environment")
        self.clock = pygame.time.Clock()

        self.ecrs = []
        self.scrs = []
        self.lifespans = []

    def simulate(self):
        running = True
        while running and self.sun.day < 5:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            self.screen.fill(self.BACKGROUND)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.sun.draw(self.screen)

            dead = []
            birthed = []
            for i, plant in enumerate(self.plants):
                code = plant.pass_time(self.sun)
                if code == 1:
                    birthed.append(plant.birth(self.WIDTH, self.HEIGHT, self.sun.day))
                if code != -1:
                    plant.draw(self.screen)
                else:
                    dead.append(i)

            for i in dead[::-1]:
                dead_plant = self.plants.pop(i)
                self.ecrs.append(dead_plant.energy_change_rate)
                self.scrs.append(dead_plant.size_change_rate)
                self.lifespans.append(self.sun.day - dead_plant.birth_date)

            for plant in birthed:
                self.plants.append(plant)

            pygame.display.flip()

            self.sun.move()

            self.clock.tick(70)
        print("Quitting pygame")
        pygame.quit()
        print("Quit pygame")
        
        for plant in self.plants:
            self.ecrs.append(plant.energy_change_rate)
            self.scrs.append(plant.size_change_rate)
            self.lifespans.append(self.sun.day - plant.birth_date)

        plt.figure(figsize=(10, 6))
        plt.scatter(self.ecrs, self.lifespans, color='blue', marker='o')

        plt.xlabel('Energy Change Rate')
        plt.ylabel('Lifespan')
        plt.title('Scatter Plot of Energy Change Rate vs. Lifespan')

        plt.grid()
        plt.show()
        print("Trying to show")

        plt.figure(figsize=(10, 6))
        plt.scatter(self.scrs, self.lifespans, color='blue', marker='o')

        plt.xlabel('Size Change Rate')
        plt.ylabel('Lifespan')
        plt.title('Scatter Plot of Size Change Rate vs. Lifespan')

        plt.grid()
        plt.show()
        
        

if __name__ == "__main__":
    env = Environment()
    env.simulate()

