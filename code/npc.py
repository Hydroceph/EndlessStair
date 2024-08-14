
""" NPC sprites: props, weapons and enemies """

import pygame
from graphics import TILESIZE

# static background props

class Prop(pygame.sprite.Sprite):
	def __init__(self,pos,groups,surface = pygame.Surface((TILESIZE,TILESIZE)), inflatex = 0, inflatey = 0):
		super().__init__(groups)
		self.image = surface
		self.rect = self.image.get_rect(topleft = pos)
		self.rect_collision = self.rect.inflate(inflatex, inflatey)

class TransitionSprite(Prop):
    def __init__(self, pos, groups, surface=pygame.Surface((TILESIZE, TILESIZE)), inflatex=0, inflatey=0, target = 'dung_room_1'):
        super().__init__(pos, groups, surface, inflatex, inflatey)

        self.target = target
        # could expand on this to import targets from Tiled, letting you go back and forth between levels, if added in the Overworld