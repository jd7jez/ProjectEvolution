import pygame

class Plant:
    def __init__(self, x, y, initial_energy=30.0, energy_change_rate=1.0, size_change_rate=1.0):
        self.x = x
        self.y = y
        self.energy = initial_energy
        self.energy_change_rate = energy_change_rate
        self.size_change_rate = size_change_rate
        self.size = 10.0
        self.color1 = int(200 * (self.energy_change_rate / 3.0))
        self.color3 = int(200 * (self.size_change_rate / 2.0))
        self.vitality = 100

    def draw(self, surface):
        green_score = int(255 * (self.vitality / 100)) if self.vitality > 0 else 0
        pygame.draw.circle(surface, (self.color1, green_score, self.color3), (self.x, self.y), self.size)

    def pass_time(self, sun):
        # Decrease the energy based on the size of the plant and then increase based on sunlight
        # Both of these changes will be scaled based on the energy change rate
        base_energy_lost = self.size // 10 if self.size // 10 > 0 else (1 if self.energy > 0 else 0)
        self.energy -= base_energy_lost * self.energy_change_rate
        base_energy_gained = sun.give_energy(self.x)
        self.energy += base_energy_gained * self.energy_change_rate
        if self.energy >= 10:
            if self.vitality < 100:
                self.vitality += 1
            if self.energy > 30:
                self.size += self.size_change_rate
        elif self.energy < 10:
            if self.size > 5:
                self.size -= self.size_change_rate
            else:
                self.vitality -= 1
        if self.vitality == 0:
            return -1
        else:
            return 0