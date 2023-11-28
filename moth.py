import pygame
import math
import random

class Moth:
    def __init__(self):
        self.x = random.randint(1, 1280)
        self.y = random.randint(1, 720)
        self.angle = 0
        self.velocity = 3
        self.radius = 8

    def draw(self, win):
        #SIMPLE DOMAIN
        pygame.draw.circle(win, (100, 100, 100), (self.x, self.y), 50)
        #moth
        pygame.draw.circle(win, (255, 0, 0), (self.x, self.y), self.radius)
        #fov
        pygame.draw.line(win, (0, 255, 0), (self.x, self.y), (self.x - math.sin(self.angle) * 50, self.y + math.cos(self.angle) * 50), 3)
        

    # RANDOM MOVEMENT
    def move(self):
        if self.x <= 0 or self.x >= 1280:
            self.angle = math.pi - self.angle
        if self.y <= 0 or self.y >= 720:
            self.angle = -self.angle

        self.x += self.velocity * math.cos(self.angle)
        self.y += self.velocity * math.sin(self.angle)

    # UNCOMMENT FOR TESTING
    # def move(self):
    #     sin_a = math.sin(self.angle)
    #     cos_a = math.cos(self.angle)
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_a]:
    #         self.x += self.velocity * cos_a
    #         self.y += self.velocity * sin_a
    #     if keys[pygame.K_d]:
    #         self.x += -self.velocity * cos_a
    #         self.y += -self.velocity * sin_a
    #     if keys[pygame.K_s]:
    #         self.x += self.velocity * sin_a
    #         self.y += -self.velocity * cos_a
    #     if keys[pygame.K_w]:
    #         self.x += -self.velocity * sin_a
    #         self.y += self.velocity * cos_a
    #     if keys[pygame.K_LEFT]:
    #         self.angle -= 0.03
    #     if keys[pygame.K_RIGHT]:
    #         self.angle += 0.03

    def move_forward(self):
        self.x = self.x + self.speed * math.cos(self.angle * math.pi / 180)
        self.y = self.y + self.speed * math.sin(self.angle * math.pi / 180)
        if self.energy > 0:
            self.energy -= self.move_cost 

    def turn_left(self):
        self.angle -= 5
        self.angle %= 360
            
    def turn_right(self):
        self.angle += 5
        self.angle %= 360
    
    # def reach(self, foods):
    #     closest_distance = float('inf')
    #     closest_moth = None

    #     for food in foods:
    #         distance_to_food = math.hypot(food.x - self.x, food.y - self.y)
    #         if distance_to_food < closest_distance:
    #             closest_distance = distance_to_food
    #             closest_moth = food
    #             return [closest_distance, (self.x, self.y), (food.x, food.y)] 
