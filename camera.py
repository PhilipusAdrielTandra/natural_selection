import os
import pygame

MENU_COLOR = (34, 116, 165)
MENU_TEXT_COLOR = (255,255,255)
MENU_Y_HEIGHT = 720/1.5 #650 # Height that seperates simulation from options tab
STAT_FONT = pygame.font.Font("Afacad-Regular.ttf", 30)

class Camera:
    def __init__(self, zoom_scale, settings, map):
        self.zoom_scale = zoom_scale
        self.scale_factor = 0.1
        self.max_zoom_level = 2.2
        self.camera_move_speed = 50
        self.offset = pygame.math.Vector2(100,500)
        self.map = map
        self.internal_surface = pygame.Surface(self.map.INTERNAL_SURFACE_SIZE, pygame.SRCALPHA)
        self.settings = settings

    def scale_up(self):
        if self.zoom_scale <= self.max_zoom_level:
            self.zoom_scale += self.scale_factor
        self.zoom_scale = round(self.zoom_scale, 2)
    
    def scale_down(self):
        if self.zoom_scale >= 2*self.scale_factor:
            self.zoom_scale -= self.scale_factor
        self.zoom_scale = round(self.zoom_scale, 2)

    def move_camera_left(self):
        self.offset.x += self.camera_move_speed
    
    def move_camera_right(self):
        self.offset.x -= self.camera_move_speed
    
    def move_camera_up(self):
        self.offset.y += self.camera_move_speed

    def move_camera_down(self):
        self.offset.y -= self.camera_move_speed
    
    def draw_window(self, win, stats, buttons, foods, organisms, vision_lines, angle_difference_stat, generation, config): 
        
        # Clear everything
        win.fill((0,0,0))
        self.internal_surface.fill((255,255,255)) 
        
        # Draw simulation on surface
        for food in foods:
            if food.has_been_eaten == False:
                food.draw(self.internal_surface)
        for organism in organisms:
            organism.draw(self.internal_surface, self.settings)
        for line in vision_lines:
            pygame.draw.line(self.internal_surface, "black", line[0], line[1], 2) 
        stats.draw_selected_org(self.internal_surface)

        # scale the surface
        scaled_surf = pygame.transform.scale(self.internal_surface, self.map.INTERNAL_SURFACE_SIZE_VECTOR * self.zoom_scale)
        
        # Blit surface on the window
        win.blit(scaled_surf, scaled_surf.get_rect(center=(win.get_size()[0]/2+self.offset.x,win.get_size()[1]/2+self.offset.y)))
     
        # Draw menu (with stats etc) on window on top of simulation surface
        pygame.draw.rect(win, MENU_COLOR, pygame.Rect(0, MENU_Y_HEIGHT, win.get_size()[0], win.get_size()[1]-MENU_Y_HEIGHT))
        pygame.draw.line(win, "black", (0, MENU_Y_HEIGHT), (win.get_size()[0], MENU_Y_HEIGHT), 2)
        for button in buttons:
            button.draw(win) 

        settings_text = STAT_FONT.render("SETTINGS", 1, MENU_TEXT_COLOR)
        settings_text = pygame.transform.rotate(settings_text, 90)
        pygame.draw.line(win, (0,0,0), (400, MENU_Y_HEIGHT), (400, MENU_Y_HEIGHT + 310), 5)
        pygame.draw.line(win, (0,0,0), (480, MENU_Y_HEIGHT), (480, MENU_Y_HEIGHT + 310), 5)
        win.blit(settings_text, (425, MENU_Y_HEIGHT + 55))
        
        stats_text = STAT_FONT.render("STATISTICS", 1, MENU_TEXT_COLOR)
        stats_text = pygame.transform.rotate(stats_text, 90)
        org_count_text = STAT_FONT.render("Organisms: " + str(len(organisms)), 1, MENU_TEXT_COLOR)
        gen_text = STAT_FONT.render("Generation: " + str(generation), 1, MENU_TEXT_COLOR)
        zoom_level_text = STAT_FONT.render("Zoom: " + str(self.zoom_scale), 1, MENU_TEXT_COLOR)
        angle_difference_text = STAT_FONT.render("Angle diff: " + str(round(angle_difference_stat)), 1, MENU_TEXT_COLOR)

        pygame.draw.line(win, (0,0,0), (725, MENU_Y_HEIGHT), (725, MENU_Y_HEIGHT + 310), 5)
        pygame.draw.line(win, (0,0,0), (825, MENU_Y_HEIGHT), (825, MENU_Y_HEIGHT + 310), 5)
        
        pygame.draw.line(win, (0,0,0), (100, MENU_Y_HEIGHT), (100, MENU_Y_HEIGHT + 310), 5)
        win.blit(stats_text, (30, MENU_Y_HEIGHT + 50)) 
        win.blit(org_count_text, (150, MENU_Y_HEIGHT + 40)) 
        win.blit(gen_text, (150, MENU_Y_HEIGHT+80)) 
        win.blit(zoom_level_text, (150, MENU_Y_HEIGHT+120)) 
        win.blit(angle_difference_text, (150, MENU_Y_HEIGHT+160)) 

        stats.draw_stats(win) 
        
        if self.settings.draw_nn:
            stats.draw_net(config, win, node_names={-1:"angle diff", -2:"distance", 0:"forward", 1:"left", 2:"right"}, draw_node_names=self.settings.draw_node_names)
        
        pygame.display.update()