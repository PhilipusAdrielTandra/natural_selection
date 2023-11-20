import pygame
import math
import random
import sys
import os
from moth import Moth
from food import Food
import neat

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
food = Food()
moth = Moth()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    food.draw(screen)
    moth.draw(screen)
    moth.move()
    pygame.display.flip()

    clock.tick(60) 

pygame.quit()
