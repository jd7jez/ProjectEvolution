import pygame
import time
from Sun import Sun
from Plant import Plant
import random

class Environment:
    def __init__(self, width=1200, height=800):
        self.WIDTH = width
        self.HEIGHT = height

        self.BACKGROUND = (255, 255, 255)
        self.sun = Sun(150, self.WIDTH, self.HEIGHT, self.WIDTH, 8)
        self.plants = [Plant(random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT), 30.0,
                             energy_change_rate=(random.random() * 2.75) + 0.25, size_change_rate=(random.random() * 1.5) + 0.5)
                       for _ in range(100)]

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Environment")
        self.clock = pygame.time.Clock()

        self.simulate()

    def simulate(self):
        running = True
        while running:
            self.screen.fill(self.BACKGROUND)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.sun.draw(self.screen)

            dead = []
            for i, plant in enumerate(self.plants):
                code = plant.pass_time(self.sun)
                if code != -1:
                    plant.draw(self.screen)
                else:
                    dead.append(i)

            for i in dead[::-1]:
                self.plants.pop(i)

            pygame.display.flip()

            self.sun.move()

            self.clock.tick(10)

if __name__ == "__main__":
    env = Environment()
    env.simulate()

