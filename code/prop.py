
""" Basic visible background sprites """

import pygame 

class Prop(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.image = pygame.image.load('./graphics/overworld/test/rock.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.rect_collision = self.rect.inflate(0, -10)