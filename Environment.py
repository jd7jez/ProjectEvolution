import pygame
import time
from Sun import Sun
from Plant import Plant
import random
import matplotlib.pyplot as plt
import sys
from concurrent.futures import ThreadPoolExecutor

class Environment:
    def __init__(self, width=1400, height=900):
        self.WIDTH = width
        self.HEIGHT = height
        # Old ECR: 0.25-3.0
        # OLD SCR: 0.5-2.0
        self.BACKGROUND = (255, 255, 255)
        self.sun = Sun(self.WIDTH, self.HEIGHT, self.WIDTH, 10)
        self.plant_squares = [[0 for _ in range((self.WIDTH // 50) + 1)] for _ in range((self.HEIGHT // 50) + 1)]
        self.plants = [Plant(random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT), 0, 50.0,
                             energy_change_rate=(random.random() *4.75) + 0.25, size_change_rate=(random.random() * 3.5) + 0.5)
                       for _ in range(50)]

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Environment")
        self.clock = pygame.time.Clock()

        self.ecrs = []
        self.scrs = []
        self.lifespans = []

    def process_plant(self, plant):
        x_i = plant.x // 50
        y_i = plant.y // 50
        code = plant.pass_time(self.sun, self.plant_squares[y_i][x_i])
        birth = None
        if code == 1:
            birth = plant.birth(self.WIDTH, self.HEIGHT, self.sun.day)
        if code != -1:
            plant.draw(self.screen)
        return (plant, code, birth)

    def simulate(self):
        running = True
        while running and self.sun.day < 15:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.plant_squares = [[0 for _ in range((self.WIDTH // 50) + 1)] for _ in range((self.HEIGHT // 50) + 1)]
            for plant in self.plants:
                x_i = plant.x // 50
                y_i = plant.y // 50
                self.plant_squares[y_i][x_i] += 1
                    
            self.screen.fill(self.BACKGROUND)

            self.sun.draw(self.screen)

            with ThreadPoolExecutor() as executor:
                plant_results = list(executor.map(self.process_plant, self.plants))

            dead = []
            birthed = []
            for i, (plant, code, birth) in enumerate(plant_results):
                if code == 1:
                    birthed.append(birth)
                if code == -1:
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

        pygame.quit()
        
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

