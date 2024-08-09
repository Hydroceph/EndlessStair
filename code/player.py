
""" Player controlled sprite """

import pygame
from graphics import png_collection

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites,create_projectile):
		super().__init__(groups)

		# sprite initial creation
		self.image = pygame.image.load('./graphics/underworld/Heroes/Wizzard/Idle/collection/Idle-Sheet-1.png').convert_alpha()
		self.image = pygame.transform.scale_by(self.image, 3)
		self.rect = self.image.get_rect(topleft = pos)
		self.rect_collision = self.rect.inflate(-15, -30)

		# graphical variables
		self.player_graphics = {
			'Wiz_Idle': png_collection('./graphics/underworld/Heroes/Wizzard/Idle/collection'),
			'Wiz_Run': png_collection('./graphics/underworld/Heroes/Wizzard/Run/collection')
		}
		self.status = 'right'
		self.frame_index = 0
		self.animation_speed = 0.15
		self.create_projectile = create_projectile

		# movement + attack variables
		self.direction = pygame.math.Vector2()
		self.pri_attack = False
		self.sec_attack = False
		self.cooldown_time = 400 # in milliseconds
		self.last_pri_attack_time = None
		self.last_sec_attack_time = None

		self.obstacle_sprites = obstacle_sprites

		# stats
		self.stats = {'health': 100, 'attack': 10, 'speed': 6}
		self.health = self.stats['health']
		self.speed = self.stats['speed']
		self.exp = 10

	def input(self):
		# checking for all inputs, using wasd for movement
		keys = pygame.key.get_pressed()

		# movement
		# up/down input
		if keys[pygame.K_w]:
			self.direction.y = -1
			if 'idle' in self.status:
				self.status = self.status.replace('_idle', '')
		elif keys[pygame.K_s]:
			self.direction.y = 1
			if 'idle' in self.status:
				self.status = self.status.replace('_idle', '')
		else:
			self.direction.y = 0
		
		# left/right input
		if keys[pygame.K_a]:
			self.direction.x = -1
			self.status = 'left'
		elif keys[pygame.K_d]:
			self.direction.x = 1
			self.status = 'right'
		else:
			self.direction.x = 0
	
		# primary attack
		if keys[pygame.K_SPACE] and self.pri_attack == False:
			print('i am dumb')
			self.create_projectile()
			self.pri_attack = True
			self.last_pri_attack_time = pygame.time.get_ticks()

		# secondary attack
		if keys[pygame.K_LSHIFT] and self.sec_attack == False:
			print('i am dumber')
			self.sec_attack = True
			self.last_sec_attack_time = pygame.time.get_ticks()

	def action_status(self):

		# idle - makes it right_idle or left_idle, which can then be used to flip image so player looks left or right as needed
		if self.direction.x == 0 and self.direction.y == 0:
			if 'idle' in self.status:
				pass
			else:
				self.status = self.status + '_idle'

	def animate(self):
		self.frame_index += self.animation_speed
		if 'idle' in self.status:
			animation_key = 'Wiz_Idle'
		else: # running
			animation_key = 'Wiz_Run'

		animation = self.player_graphics[animation_key]
		if self.frame_index > len(animation):
			self.frame_index = 0


		self.image = animation[int(self.frame_index)]
		self.image = pygame.transform.scale_by(self.image, 3)
		if 'left' in self.status:
			self.image = pygame.transform.flip(self.image,True,False)
		self.rect = self.image.get_rect(center = self.rect_collision.center)

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

	def attack_cooldown(self):
		current_time = pygame.time.get_ticks()

		# player attacking
		if self.pri_attack == True:
			if current_time - self.last_pri_attack_time >= self.cooldown_time:
				self.pri_attack = False

		if self.sec_attack == True:
			if current_time - self.last_sec_attack_time >= self.cooldown_time:
				self.sec_attack = False

		# player being attacked?

	def update(self):
		self.input()
		self.attack_cooldown()
		self.action_status()
		self.animate()
		self.move(self.speed)