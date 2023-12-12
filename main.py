import time
import os
import random
import math

import pygame
import neat
from numpy import array

from ui import Button, draw_net2
from ui import StatsScreen
from utils import calculate_angle, calculate_distance, calculate_angle_diff
from utils import KdTree
from camera import Camera
from entity import Moth, Food

pygame.font.init()
MENU_Y_HEIGHT = 700 
MENU_COLOR = (34, 116, 165)
MENU_TEXT_COLOR = (255,255,255)
FPS = 60

def get_population_size_from_file():
    with open('config-feedforward.txt') as f:
        for line in f:
            if "pop_size" in line:
                test = line.split()
                return int(test[-1])

POPULATION_SIZE = get_population_size_from_file()
generation = 0

class Settings():
    def __init__(self):
        self.draw_vision_lines = True
        self.paused = False
        self.draw_nn = False
        self.draw_node_names = False

class Map():
    def __init__(self):
        self.INTERNAL_SURFACE_SIZE = (3000, 3000)
        self.INTERNAL_SURFACE_SIZE_VECTOR = pygame.math.Vector2(self.INTERNAL_SURFACE_SIZE)

map = Map()
settings = Settings()
camera = Camera(0.8, settings, map)
all_orgsanism_dictonary = {}

def main(genomes, config): 
    global generation
    generation += 1 
    
    nets = []
    ge = []
    organisms = []
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        new_size = 1 if (g.parent_key1 is None or g.parent_key2 is None) else (all_orgsanism_dictonary[g.parent_key1].size_factor + all_orgsanism_dictonary[g.parent_key2].size_factor)/2
        new_speed = 0 if (g.parent_key1 is None or g.parent_key2 is None) else (all_orgsanism_dictonary[g.parent_key1].speed_factor + all_orgsanism_dictonary[g.parent_key2].speed_factor)/2
        new_vision = 0 if (g.parent_key1 is None or g.parent_key2 is None) else (all_orgsanism_dictonary[g.parent_key1].vision_factor + all_orgsanism_dictonary[g.parent_key2].vision_factor)/2
        organisms.append(Moth(new_size, new_speed, new_vision, random.randrange(0, map.INTERNAL_SURFACE_SIZE[0]), MENU_Y_HEIGHT, g.key, g.parent_key1, g.parent_key2, g))
        all_orgsanism_dictonary[g.key] = organisms[-1]
        g.fitness = 0
        ge.append(g)
        #print( g.key, " = ", g.parent_key1, " + ", g.parent_key2)

    run = True
    win = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    button_pause = Button("Pause", (900, MENU_Y_HEIGHT+180), font_size=38)
    button_change_style = Button("Draw vision", (900, MENU_Y_HEIGHT+250), font_size=38, pressed=not settings.draw_vision_lines)
    button_draw_nn = Button("Draw nn", (900, MENU_Y_HEIGHT+320), font_size=38, pressed=not settings.draw_nn)
    button_draw_nn_node_names = Button("Node names", (900, MENU_Y_HEIGHT+390), font_size=38, pressed=not settings.draw_node_names)
    button_exit = Button("EXIT", (win.get_size()[0] - 100, 20), font_size=40, pressed=False)
    # button_zoom = Button("ZOOM", (win.get_size()[0] - 200, 100), font_size=40, pressed=False)
    # button_unzoom = Button("UNZOOM", (win.get_size()[0] - 200, 180), font_size=40, pressed=False)
    foods = []
    
    for _ in range(800):
        foods.append(Food("green", map))

    all_food = [[food.x,food.y, food] for food in foods]
    all_org = [[*org.img.get_rect(topleft = (org.x, org.y)).center, org] for org in organisms]
    # all_food.extend(all_org)
    food_kd_tree = KdTree(all_food)
        
    stats = StatsScreen(organisms[0], win.get_size()[0], win.get_size()[1], MENU_Y_HEIGHT, MENU_TEXT_COLOR)
    
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEWHEEL:
                if event.y < 0:
                    camera.scale_down()
                if event.y > 0:
                    camera.scale_up()
            
            if button_exit.click(event):
                run = False
                pygame.quit()
                quit()
            
            # if button_zoom.click(event):
            #     camera.scale_up()

            # if button_unzoom.click(event):
            #     camera.scale_down()
            
            if button_pause.click(event):
                settings.paused = not settings.paused
            
            if button_change_style.click(event):
                settings.draw_vision_lines = not settings.draw_vision_lines
            
            if button_draw_nn.click(event):
                settings.draw_nn = not settings.draw_nn
            
            if button_draw_nn_node_names.click(event):
                settings.draw_node_names = not settings.draw_node_names
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    settings.paused = not settings.paused
                    button_pause.increase_tick() 
                if event.key == pygame.K_q:
                    camera.scale_up()
                if event.key == pygame.K_e:
                    camera.scale_down()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    camera.move_camera_up()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    camera.move_camera_down()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    camera.move_camera_left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    camera.move_camera_right()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    for organism in organisms:
                        organism.click(stats, win, camera, map)
        
        if settings.paused:
            camera.draw_window(win, stats, [button_pause, button_change_style, button_draw_nn, button_draw_nn_node_names, button_exit], foods, organisms, vision_lines, angle_difference_stat, generation, config)
            continue
        
        if len(organisms) <= 0:
            run = False
            break
        
        vision_lines = []
        angle_difference_stat = 0
        for i, organism in enumerate(organisms):
            organism.live()

            min_dist = 100 
            closest_object = None 
            org_center_x, org_center_y = organism.img.get_rect(topleft = (organism.x, organism.y)).center
            search_box = array([[org_center_x-organism.vision_radius, org_center_x+organism.vision_radius], [org_center_y-organism.vision_radius, org_center_y+organism.vision_radius]])
            for point in food_kd_tree.range_search(search_box):
                food = point[2]

                if food.TYPE == "FOOD":
                    if food.has_been_eaten:
                        continue

                    if organism.collides(food) == True:
                        if food.TYPE == "FOOD":
                            organism.energy += food.energy
                            ge[i].fitness += 5 
                            food.has_been_eaten = True
                    
                    object_in_vision_coords = organism.reach(food)
                    if object_in_vision_coords != None:
                        if settings.draw_vision_lines:
                            vision_lines.append(object_in_vision_coords)
                        
                        dist = calculate_distance(object_in_vision_coords[0], object_in_vision_coords[1])
                        if dist < min_dist:
                            min_dist = dist
                            closest_object = object_in_vision_coords

                if food.TYPE == "ORGANISM":
                    pass
            
            if closest_object is not None and (abs((organism.angle%360)-calculate_angle(closest_object[0], closest_object[1]))) < 7:
                ge[i].fitness += 0.2
            ge[i].fitness += 1
                
            if closest_object is not None:
                angle_difference = calculate_angle_diff(organism.angle, calculate_angle(closest_object[0], closest_object[1], invert=1))
                ge[i].fitness += (organism.vision_radius/50)/(calculate_distance(closest_object[0], closest_object[1])+1)
                output = nets[i].activate([angle_difference, calculate_distance(closest_object[0], closest_object[1])])
            else:
                angle_difference = 0
                ge[i].fitness -= 0.05
                output = nets[i].activate([angle_difference, 1000])

            if organism == stats.organism:
                angle_difference_stat = angle_difference

            if output[0] > 0.5:
                organism.move_forward()
            if output[1] > 0.5:
                organism.turn_left()
            elif output[2] > 0.5:
                organism.turn_right()

            if organism.health <= 0:
                ge[i].fitness -= 1
                organisms.pop(i)
                nets.pop(i)
                ge.pop(i)

        camera.draw_window(win, stats, [button_pause, button_change_style, button_draw_nn, button_draw_nn_node_names, button_exit], foods, organisms, vision_lines, angle_difference_stat, generation, config)

class MyGenome(neat.DefaultGenome):

    def __init__(self, key):
        super().__init__(key)
        self.parent_key1 = None
        self.parent_key2 = None

    def configure_crossover(self, genome1, genome2, config):
        self.parent_key1 = genome1.key
        self.parent_key2 = genome2.key
        super().configure_crossover(genome1, genome2, config)
    
def run(config_path):
    config = neat.config.Config(MyGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    p = neat.Population(config)
    
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 200) 

if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, "config-feedforward.txt")
    run(config_path)