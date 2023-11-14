import pygame
import math
import random

class Moth:
    def __init__(self):
        self.x = random.randint(1, 1280)
        self.y = random.randint(1, 720)
        self.angle = 0
        self.velocity = 5
        self.radius = 5

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.velocity
        self.y += self.velocity
    

        