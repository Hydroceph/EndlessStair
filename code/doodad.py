
""" Basic visible, colidable background sprites. All rocks, trees, bridges etc. """

import pygame 
from settings import *

class Doodad(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.image = pygame.image.load('./graphics/overworld/test/rock.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.rect_collision = self.rect.inflate(0, -10)