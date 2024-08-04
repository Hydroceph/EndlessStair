
""" Player controlled sprite """

import pygame 
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)

		self.image = pygame.image.load('./graphics/overworld/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.rect_collision = self.rect.inflate(-5, -20)

		self.direction = pygame.math.Vector2()
		self.speed = 5

		self.obstacle_sprites = obstacle_sprites

	def input(self):
		# checking for all inputs, using wasd for movement
		keys = pygame.key.get_pressed()

		# up/down input
		if keys[pygame.K_w]:
			self.direction.y = -1
		elif keys[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0
		
		# left/right input
		if keys[pygame.K_a]:
			self.direction.x = -1
		elif keys[pygame.K_d]:
			self.direction.x = 1
		else:
			self.direction.x = 0
	
	def move(self,speed):
		# diagonal movement
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		# movement with collision check
		self.rect_collision.y += self.direction.y * speed
		self.collision('vertical')
		self.rect_collision.x += self.direction.x * speed
		self.collision('horizontal')
		self.rect.center = self.rect_collision.center


	def collision(self,direction):
		# up/down collision
		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.rect_collision.colliderect(self.rect_collision):
					# moving down
					if self.direction.y > 0:
						self.rect_collision.bottom = sprite.rect_collision.top
					# moving up
					if self.direction.y < 0:
						self.rect_collision.top = sprite.rect_collision.bottom

		# left/right collision
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.rect_collision.colliderect(self.rect_collision):
					# moving right
					if self.direction.x > 0:
						self.rect_collision.right = sprite.rect_collision.left
					# moving left
					if self.direction.x < 0:
						self.rect_collision.left = sprite.rect_collision.right

	def update(self):
		self.input()
		self.move(self.speed)