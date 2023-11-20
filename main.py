import pygame
import math
import random
from moth import Moth
from food import Food

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
food = Food()
moths = [Moth()]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            moths.append(Moth())

    screen.fill("white")
    food.draw(screen)

    for i, moth1 in enumerate(moths):
        moth1.draw(screen)
        moth1.move()

        if math.hypot(moth1.x - food.x, moth1.y - food.y) < moth1.radius + food.size[0]/2:
            food.eaten = True

        for j, moth2 in enumerate(moths):
            if i != j:
                if math.hypot(moth1.x - moth2.x, moth1.y - moth2.y) < moth1.radius + moth2.radius:
                    pass

    if food.eaten:
        food = Food()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
