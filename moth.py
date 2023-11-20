import pygame
import math
import random

class Moth:
    def __init__(self):
        self.x = random.randint(1, 1280)
        self.y = random.randint(1, 720)
        self.angle = random.uniform(0, 2 * math.pi)
        self.velocity = 3
        self.radius = 8

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius)

    def move(self):
        if self.x <= 0 or self.x >= 1280:
            self.angle = math.pi - self.angle
        if self.y <= 0 or self.y >= 720:
            self.angle = -self.angle

        self.x += self.velocity * math.cos(self.angle)
        self.y += self.velocity * math.sin(self.angle)
