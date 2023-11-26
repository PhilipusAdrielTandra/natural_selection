import pygame
import math
import random

class Food:
    def __init__(self):
        self.x = random.randint(1, 1280)
        self.y = random.randint(1, 720)
        self.size = 4
        self.energy = 50
        self.eaten = False

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 255), (self.x, self.y), self.size)