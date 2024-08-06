
""" NPC sprites """

import pygame 
from map import TILESIZE

class Prop(pygame.sprite.Sprite):
	def __init__(self,pos,groups,surface = pygame.Surface((TILESIZE,TILESIZE))):
		super().__init__(groups)
		self.image = surface
		self.rect = self.image.get_rect(topleft = pos)
		self.rect_collision = self.rect

class StaticProp(Prop):
	def __init__(self, pos, groups, surface=pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(pos, groups, surface)
		self.rect_collision = self.rect.inflate(-8, -42)

