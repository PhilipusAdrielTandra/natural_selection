import pygame
import math
import random
from moth import Moth
from food import Food
import neat

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
foods = [Food() for i in range(10)]
moths = [Moth() for i in range(5)]

nets = []
ge = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")

    for food in foods:
        food.draw(screen)

    # Collision
    for moth in moths:
        moth.draw(screen)
        moth.move()

        for food in foods:
            if math.hypot(moth.x - food.x, moth.y - food.y) < moth.radius + food.size:
                food.eaten = True

    foods = [food for food in foods if not food.eaten]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
