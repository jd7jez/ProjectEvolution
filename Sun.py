import pygame

class Sun:
    def __init__(self, sun_width, env_width, env_height, start, speed, ring2=3, ring3=2, energy_yields=[15, 10, 5]):
        self.WIDTH = sun_width
        self.HEIGHT = env_height
        self.pos = start
        self.speed = speed
        self.energy_yields = energy_yields
        self.YELLOW1 = (255, 255, 0)
        self.YELLOW2 = (200, 200, 0)
        self.YELLOW3 = (150, 150, 0)

        self.ring2_ratio = ring2
        self.ring3_ratio = ring3

        self.min_pos = 0 - ((self.WIDTH // 2) + (self.WIDTH // self.ring3_ratio))
        self.max_pos = env_width + ((self.WIDTH // 2) + (self.WIDTH // self.ring3_ratio))

        self.day = 0

    def move(self):
        self.pos -= self.speed
        if self.pos < self.min_pos:
            self.pos = self.max_pos
            self.day += 1

    def draw(self, surface):
        pygame.draw.rect(surface, self.YELLOW3, ((self.pos - ((self.WIDTH // 2) + (self.WIDTH // self.ring3_ratio))), 0, self.WIDTH + (2 * (self.WIDTH // self.ring3_ratio)), self.HEIGHT))
        pygame.draw.rect(surface, self.YELLOW2, ((self.pos - ((self.WIDTH // 2) + (self.WIDTH // self.ring2_ratio))), 0, self.WIDTH + (2 * (self.WIDTH // self.ring2_ratio)), self.HEIGHT))
        pygame.draw.rect(surface, self.YELLOW1, (self.pos - (self.WIDTH // 2), 0, self.WIDTH, self.HEIGHT))
        font = pygame.font.Font(None, 36)
        day_text = font.render(f"Day: {self.day}", True, (0, 0, 0))
        surface.blit(day_text, (10, 10))

    def give_energy(self, x):
        if x > self.pos - (self.WIDTH // 2) and x < self.pos + (self.WIDTH // 2):
            return 15
        if x > self.pos - ((self.WIDTH // 2) + (self.WIDTH // self.ring2_ratio)) and x < self.pos + ((self.WIDTH // 2) + (self.WIDTH // self.ring2_ratio)):
            return 10
        if x > self.pos - ((self.WIDTH // 2) + (self.WIDTH // self.ring3_ratio)) and x < self.pos + ((self.WIDTH // 2) + (self.WIDTH // self.ring3_ratio)):
            return 5
        return 0