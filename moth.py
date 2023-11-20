import pygame
import math
import random

class Moth:
    def __init__(self):
        self.x = random.randint(1, 1280)
        self.y = random.randint(1, 720)
        self.angle = 0
        self.velocity = 5
        self.radius = 8

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius)

    #input for testing
    def move(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x += self.velocity * cos_a
            self.y += self.velocity * sin_a
        if keys[pygame.K_d]:
            self.x += -self.velocity * cos_a
            self.y += -self.velocity * sin_a
        if keys[pygame.K_s]:
            self.x += self.velocity * sin_a
            self.y += -self.velocity * cos_a
        if keys[pygame.K_w]:
            self.x += -self.velocity * sin_a
            self.y += self.velocity * cos_a
        if keys[pygame.K_LEFT]:
            self.angle -= 0.03
        if keys[pygame.K_RIGHT]:
            self.angle += 0.03
    

        