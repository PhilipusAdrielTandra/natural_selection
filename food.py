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

    def draw(self, win, moths):
        closest_distance = float('inf')
        closest_moth = None

        for moth in moths:
            distance_to_moth = math.hypot(self.x - moth.x, self.y - moth.y)
            if distance_to_moth < closest_distance:
                closest_distance = distance_to_moth
                closest_moth = moth

        print(closest_distance)
        if closest_distance <= 50:
            color = (255, 0, 0)
        else:
            color = (0, 0, 255)

        pygame.draw.circle(win, color, (self.x, self.y), self.size)