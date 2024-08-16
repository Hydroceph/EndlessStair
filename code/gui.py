
""" Shows the player health and exp on screen """

import pygame
from game_data import FONT, FONT_SIZE, WIDTH, HEIGHT, BAR_HEIGHT, HEALTH_COLOUR, EXP_FONT_COLOUR, BAR_BACKGROUND_COLOUR, HP_BAR_WIDTH, BAR_BORDER_COLOUR 


class GUI:
    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, FONT_SIZE)

        # health bar, corrected to centre of screen just under the player
        self.hp_width = (WIDTH / 2) - 48
        self.hp_height = (HEIGHT / 2) + 64
        self.hp_bar_rect = pygame.Rect(self.hp_width,self.hp_height,HP_BAR_WIDTH, BAR_HEIGHT)

    def show_bar_portion(self,current,max_amount,background_rectangle,colour):
        # background of bar
        pygame.draw.rect(self.display_surface, BAR_BACKGROUND_COLOUR, background_rectangle)

        # converting to pixel proportion
        ratio = current / max_amount
        actual_width = background_rectangle.width * ratio
        actual_rectangle = background_rectangle.copy()
        actual_rectangle.width = actual_width

        # actual bar
        pygame.draw.rect(self.display_surface, colour, actual_rectangle)
        # actual bar border
        pygame.draw.rect(self.display_surface, BAR_BORDER_COLOUR, background_rectangle, 3)

    def show_exp(self,exp):
        exp_surface = self.font.render(str(exp), False, EXP_FONT_COLOUR)
        exp_rectangle = exp_surface.get_rect(topleft = (16,16))

        # background
        pygame.draw.rect(self.display_surface, BAR_BACKGROUND_COLOUR, exp_rectangle.inflate(8,8))
        # background border
        pygame.draw.rect(self.display_surface, BAR_BORDER_COLOUR, exp_rectangle.inflate(16,16),3)
        # exp text
        self.display_surface.blit(exp_surface, exp_rectangle)

    def display(self, player):
        self.show_bar_portion(player.health, player.stats['health'], self.hp_bar_rect, HEALTH_COLOUR)

        self.show_exp(player.exp)


