import pygame
import random

class Plant:

    health_threshold = 50
    decay_threshold = 40
    min_size = 5
    max_vitality = 100
    grow_threshold = 100
    reproduce_threshold = 400
    reproduce_chance = 0.5
    birth_cooldown_max = 10
    density_limit = 15

    def __init__(self, x, y, birth_date, initial_energy=50.0, energy_change_rate=1.0, size_change_rate=1.0):
        self.x = x
        self.y = y
        self.birth_date = birth_date
        self.energy = initial_energy
        self.energy_change_rate = energy_change_rate
        self.size_change_rate = size_change_rate
        self.size = 5.0
        self.color1 = int(255 * (self.energy_change_rate / 5.0))
        self.color3 = int(255 * (self.size_change_rate / 4.0))
        self.vitality = 100
        self.birth_cooldown = self.birth_cooldown_max

    def draw(self, surface):
        green_score = int(255 * (self.vitality / 100)) if self.vitality > 0 else 0
        pygame.draw.circle(surface, (self.color1, green_score, self.color3), (self.x, self.y), self.size)

    def pass_time(self, sun, density):
        # Decrease the energy based on the size of the plant and then increase based on sunlight
        # Both of these changes will be scaled based on the energy change rate
        base_energy_lost = self.size // 10 if self.size // 10 > 0 else (1 if self.energy > 0 else 0)
        self.energy -= base_energy_lost * self.energy_change_rate
        base_energy_gained = sun.give_energy(self.x)
        self.energy += base_energy_gained * self.energy_change_rate
        if self.energy >= self.health_threshold:
            if self.vitality < self.max_vitality:
                self.vitality += 1
            if self.energy > self.grow_threshold:
                if self.energy > self.reproduce_threshold:
                    reproduce_odds = random.random()
                    if reproduce_odds < self.reproduce_chance and density < self.density_limit:
                        if self.birth_cooldown == 0:
                            self.birth_cooldown = self.birth_cooldown_max
                            return 1
                        else:
                            self.birth_cooldown -= 1
                    else:
                        self.size += self.size_change_rate
                else:
                    self.size += self.size_change_rate
        elif self.energy < self.decay_threshold:
            if self.size > self.min_size:
                self.size -= self.size_change_rate
            else:
                self.vitality -= 1
        if self.vitality == 0:
            return -1
        else:
            return 0
    
    def birth(self, width, height, date):
        ecr_min = max(self.energy_change_rate-0.25, 0.25)
        ecr_max = min(self.energy_change_rate+0.25, 5.0)
        scr_min = max(self.size_change_rate-0.25, 0.5)
        scr_max = min(self.size_change_rate+0.25, 4.0)
        return Plant(x=random.randint(max(0, self.x-50), min(self.x+50, width)), y=random.randint(max(0, self.y-50), min(self.y+50, height)),
                     birth_date=date,
                     initial_energy=50.0,
                     energy_change_rate=(random.random() * (ecr_max - ecr_min)) + ecr_min,
                     size_change_rate=(random.random() * (scr_max - scr_min)) + scr_min)
        