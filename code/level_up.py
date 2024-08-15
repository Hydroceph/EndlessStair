import pygame
from game_data import FONT, FONT_SIZE, BAR_BACKGROUND_COLOUR, png_collection

class LevelUp:
    def __init__(self, player):
        
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.stats_names = ['health', 'attack', 'speed']

        self.max_stats = player.stats
        self.current_stats = player.current_stats
        self.exp = player.exp 

        self.stats_choice = 0
        self.choice_time = None
        self.can_change_choice = True
        self.choice_cooldown_time = 300

        self.width = self.display_surface.get_size()[0] // 3
        self.height = self.display_surface.get_size()[1] * 0.8
        self.image_list = png_collection('./graphics/level up/collection')

        self.create_upgrade_boxes()

    def menu_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and self.can_change_choice:
            if self.stats_choice < 2:
                self.stats_choice += 1
                self.can_change_choice = False
                self.choice_time = pygame.time.get_ticks()
        elif keys[pygame.K_a] and self.can_change_choice:
            if self.stats_choice > 0:
                self.stats_choice -= 1
                self.can_change_choice = False
                self.choice_time = pygame.time.get_ticks()

        if keys[pygame.K_SPACE] and self.can_change_choice:
            if self.player.exp >= 100:
                self.can_change_choice = False
                self.choice_time = pygame.time.get_ticks()
                if self.stats_choice == 0:
                    self.player.stats['health'] += 20
                    self.player.health += 20
                    self.player.exp -= 100
                elif self.stats_choice == 1:
                    self.player.stats['attack'] += 1
                    self.player.exp -= 100
                elif self.stats_choice == 2:
                    self.player.speed += 1
                    self.player.exp -= 100


    def choice_cooldown(self):
        if not self.can_change_choice:
            current_time = pygame.time.get_ticks()
            if current_time - self.choice_time >= self.choice_cooldown_time:
                self.can_change_choice = True

    def create_upgrade_boxes(self):
        self.box_list = []
        increment_nr = 0

        for box, i in enumerate(range(3)):
            # so box is 80% size of screen, starts 10% down the screen (vertically) and is equidistant between screen (horizontally) 
            increment = self.display_surface.get_size()[0] // 3
            left = increment * increment_nr
            top = self.display_surface.get_size()[1] * 0.1
            increment_nr +=1

            box = UpgradeBox(left, top, self.width, self.height, i)
            self.box_list.append(box)

    def display_level_up(self):
        self.choice_cooldown()
        self.menu_input()

        for index, box in enumerate(self.box_list):
            box.display_upgrade_box(self.display_surface, self.stats_choice, self.image_list[index])

class UpgradeBox:
    def __init__(self, left, top, width, height, index):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index

    def display_upgrade_box(self, display_surface, stats_choice, image):

        self.stats_choice = stats_choice

        self.image = image
        self.image.set_alpha(125)

        if self.index == self.stats_choice:
            self.image.set_alpha(255)
        self.surface = display_surface

        self.surface.blit(self.image, self.rect)