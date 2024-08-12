
""" Player controlled sprite """

import pygame
from graphics import png_collection, bone_weapon_data
from npc import Character

class Player(Character):
	def __init__(self, pos, groups, obstacle_sprites, create_projectile, create_melee):
		super().__init__(groups)

		# sprite initial creation
		self.image = pygame.image.load('./graphics/underworld/Heroes/Wizzard/Idle/collection/Idle-Sheet-1.png').convert_alpha()
		self.image = pygame.transform.scale_by(self.image, 3)
		self.rect = self.image.get_rect(topleft = pos)
		self.rect_collision = self.rect.inflate(-15, -30)

		# graphical variables
		self.player_graphics = {
			'Wiz_Idle': png_collection('./graphics/underworld/Heroes/Wizzard/Idle/collection'),
			'Wiz_Run': png_collection('./graphics/underworld/Heroes/Wizzard/Run/collection'),
			'Wiz_Hit': png_collection('./graphics/underworld/Heroes/Wizzard/Death/collection')
		}
		self.status = 'right'
		self.hero_type = 'Wiz'


		self.create_projectile = create_projectile
		self.create_melee = create_melee

		# movement + attack variables
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
		self.weapon_tier = bone_weapon_data
		self.current_weapon_magic = 'staff'
		self.current_weapon_melee = 'sword'
		self.player_can_be_hit = True
		self.last_hit_time = None
		self.invulnerable_time = 420
		

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
			self.create_projectile()
			self.pri_attack = True
			self.last_pri_attack_time = pygame.time.get_ticks()

		# secondary attack
		if keys[pygame.K_LSHIFT] and self.sec_attack == False:
			self.create_melee()
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
			animation_key = '_Idle'
		else: # running
			animation_key = '_Run'
		animation = self.player_graphics[self.hero_type + animation_key]
		if self.frame_index > len(animation):
			self.frame_index = 0
		self.image = animation[int(self.frame_index)]
		self.image = pygame.transform.scale_by(self.image, 3)

		if self.player_can_be_hit == False:
			self.attacked_image = self.player_graphics[self.hero_type + '_Hit'][0]
			self.attacked_image = pygame.transform.scale_by(self.attacked_image, 3)
			self.image = self.attacked_image

		if 'left' in self.status:
			self.image = pygame.transform.flip(self.image,True,False)
		self.rect = self.image.get_rect(center = self.rect_collision.center)

	def attack_cooldown(self):
		current_time = pygame.time.get_ticks()

		# player attacking - magic
		if self.pri_attack == True:
			if current_time - self.last_pri_attack_time >= self.cooldown_time + self.weapon_tier[self.current_weapon_magic]['cooldown']:
				self.pri_attack = False
		# melee
		if self.sec_attack == True:
			if current_time - self.last_sec_attack_time >= self.cooldown_time + self.weapon_tier[self.current_weapon_melee]['cooldown']:
				self.sec_attack = False

		# player being attacked?
		if self.player_can_be_hit == False:
			if current_time - self.last_hit_time >= self.invulnerable_time:
				self.player_can_be_hit = True

	def get_weapon_damage(self):
		base_damage = self.stats['attack']
		magic_weapon_damage = self.weapon_tier[self.current_weapon_magic]['damage']
		melee_weapon_damage = self.weapon_tier[self.current_weapon_melee]['damage']

		return ((magic_weapon_damage + base_damage), (melee_weapon_damage + base_damage))

	def update(self):
		if self.blocked == False:
			self.input()
			self.move(self.speed)
		self.attack_cooldown()
		self.action_status()
		self.animate()
		