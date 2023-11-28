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
            
class Moth:
    def __init__(self):
        self.x = random.randint(1, 1280)
        self.y = random.randint(1, 720)
        self.angle = 0
        self.velocity = 3
        self.radius = 8
        self.energy = 100

    def draw(self, win):
        #SIMPLE DOMAIN
        pygame.draw.circle(win, (100, 100, 100), (self.x, self.y), 50)
        #moth
        pygame.draw.circle(win, (255, 0, 0), (self.x, self.y), self.radius)
        #fov
        pygame.draw.line(win, (0, 255, 0), (self.x, self.y), (self.x - math.sin(self.angle) * 50, self.y + math.cos(self.angle) * 50), 3)
        
    # RANDOM MOVEMENT
    # def move(self):
    #     if self.x <= 0 or self.x >= 1280:
    #         self.angle = math.pi - self.angle
    #     if self.y <= 0 or self.y >= 720:
    #         self.angle = -self.angle

    #     self.x += self.velocity * math.cos(self.angle)
    #     self.y += self.velocity * math.sin(self.angle)

    # UNCOMMENT FOR TESTING
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
            self.angle -= 0.2
        if keys[pygame.K_RIGHT]:
            self.angle += 0.2

    def move_forward(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        self.x += -self.velocity * sin_a
        self.y += self.velocity * cos_a
        # if self.energy > 0:
        #     self.energy -= self.move_cost 

    def turn_left(self):
        self.angle -= 0.2
            
    def turn_right(self):
        self.angle += 0.2
    
    def reach(self, foods):
        closest_distance = float('inf')
        closest_food = None

        for food in foods:
            distance_to_food = math.sqrt((self.x - food.x) ** 2 + (self.y - food.y) ** 2)
            if distance_to_food < closest_distance:
                closest_distance = distance_to_food
                closest_food = food

        if closest_distance <= 50:
            angle_to_food = math.atan2(closest_food.y - self.y, closest_food.x - self.x)
            return angle_to_food, (self.x, self.y), (closest_food.x, closest_food.y)
        else:
            return None
