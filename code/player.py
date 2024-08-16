
""" Player controlled sprite, player weapons and player attacks """

import pygame
from game_data import WIDTH, HEIGHT, png_collection, bone_weapon_data, attack_animation_data
from character import Character
from math import atan2, degrees

class Player(Character):
	def __init__(self, pos, groups, obstacle_sprites, interactable_sprites, create_projectile, create_melee, max_stats, current_stats, exp):
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
			'Wiz_Hit': png_collection('./graphics/underworld/Heroes/Wizzard/Death/collection'),
            'Wiz_Death': png_collection('./graphics/underworld/Heroes/Wizzard/Death/collection')
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
		self.interactable_sprites = interactable_sprites

		# stats
		self.stats = max_stats
		self.current_stats = current_stats
		self.health = self.current_stats['health']
		self.speed = self.current_stats['speed']
		self.exp = exp
		self.weapon_tier = bone_weapon_data
		self.current_weapon_magic = 'staff'
		self.current_weapon_melee = 'sword'
		self.player_can_be_hit = True
		self.last_hit_time = None
		self.invulnerable_time = 420
		
		# death animation
		self.is_dead = 0

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
			self.attacked_image = self.player_graphics[self.hero_type + '_Hit'][1]
			self.attacked_image = pygame.transform.scale_by(self.attacked_image, 3)
			self.image = self.attacked_image

		if 'left' in self.status:
			self.image = pygame.transform.flip(self.image,True,False)
		self.rect = self.image.get_rect(center = self.rect_collision.center)
            
	def death_animate(self):
		self.frame_index += self.animation_speed
		animation = self.player_graphics['Wiz_Death']
		if self.frame_index > len(animation):
			self.frame_index = 0
			self.is_dead = 1
		self.image = animation[int(self.frame_index)]
		self.image = pygame.transform.scale_by(self.image, 3)
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
      
	def health_pickup(self):
		for pickup in self.interactable_sprites:
			if pickup.rect_collision.colliderect(self.rect_collision):
				self.health += 20
				if self.health >= self.stats['health']:
					self.health = self.stats['health']
				pickup.kill()

	def update(self):
		if self.blocked == False:
			self.input()
			self.move(self.speed)
		self.health_pickup()
		self.attack_cooldown()
		self.action_status()
		self.animate()
		






# player weapons

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups, weapontype, offset_fix_x = 16, offset_fix_y = 0):
        super().__init__(groups)

        self.player = player
        self.distance_from_player = 60
        self.distance_from_player_offset = pygame.math.Vector2(offset_fix_x, offset_fix_y)
        self.player_direction = pygame.Vector2(1,0)
        

        self.weapon = bone_weapon_data[weapontype]['png']
        self.weapon_surface = pygame.image.load(self.weapon).convert_alpha()
        self.weapon_surface = pygame.transform.scale_by(self.weapon_surface, 2)
        self.image = self.weapon_surface
        self.rect = self.image.get_rect(center = self.player.rect.center + self.distance_from_player_offset + self.player_direction * self.distance_from_player)

# magic weapon, always held behind player
class StaticWeapon(Weapon):
    def __init__(self, player, groups, weapontype):
        super().__init__(player, groups, weapontype)

        self.distance_from_player = 30

    def update(self):

        if 'right' in self.player.status:
            self.rect.center = self.player.rect.center + self.distance_from_player_offset + self.player_direction * (self.distance_from_player * - 1)
        else:
            self.rect.center = self.player.rect.center + self.distance_from_player_offset + self.player_direction * self.distance_from_player

# melee weapon, always held pointing towards mouse
class CQCWeapon(Weapon):
    def __init__(self, player, groups, weapontype):
        super().__init__(player, groups, weapontype)

        self.distance_from_player = 40
        self.cqc_distance_from_player_offset = pygame.math.Vector2(0,0)
        
    def update(self):
        self.weapon_direction()
        self.rotate_weapon()
        self.rect.center = self.player.rect.center + self.distance_from_player_offset - self.cqc_distance_from_player_offset + self.player_direction * self.distance_from_player

    def weapon_direction(self):
        direction = (pygame.math.Vector2(pygame.mouse.get_pos()) - pygame.math.Vector2(WIDTH / 2, HEIGHT / 2))
        self.player_direction = direction.normalize()
        
    def rotate_weapon(self):
        mouse_angle = degrees(atan2(self.player_direction.x, self.player_direction.y))
        # different substractions from mouse angle to make the sword always be facing out, could alternatively have it as -180 to be always pointing out
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.weapon_surface, (mouse_angle - 270), 1)
            
        else:
            self.image = pygame.transform.rotozoom(self.weapon_surface, ((mouse_angle - 90) * -1), 1)
            self.image = pygame.transform.flip(self.image, True, False)







# player attack
class Projectile(pygame.sprite.Sprite):
    def __init__(self,player,groups, obstacle_sprites, destructable_sprites, damageable_sprites, speed = 5, attack_type = 'nova_ball', player_distance = 75):
        super().__init__(groups)
        direction = (pygame.math.Vector2(pygame.mouse.get_pos()) - pygame.math.Vector2(WIDTH / 2, HEIGHT / 2))
        self.direction = direction.normalize()
        self.speed = speed
        
        self.attack_type = attack_type
        self.image_list = png_collection(attack_animation_data[self.attack_type])
        self.image = self.image_list[0]
        if self.attack_type == 'nova_ball':
            self.image = pygame.transform.scale_by(self.image, 0.5)

        self.rect = self.image.get_rect(center = player.rect.center + self.direction * player_distance)
        self.rect_collision = self.rect.inflate(-4, -4)

        self.frame_index = 0
        self.animation_speed = 0.3

        self.obstacle_sprites = obstacle_sprites
        self.destructable_sprites = destructable_sprites
        self.damageable_sprites = damageable_sprites

        self.magic_sound = pygame.mixer.Sound('./audio/fireball.wav')
        self.magic_sound.set_volume(0.3)
        self.magic_sound.play()

    def animate(self):
        self.frame_index += self.animation_speed
        animation = self.image_list
        if self.frame_index > len(animation):
            self.frame_index = 0
        self.image_original = animation[int(self.frame_index)]
        self.image = self.image_original
        if self.attack_type == 'nova_ball':
            self.image = pygame.transform.scale_by(self.image, 0.5)

        self.rect = self.image.get_rect(center = self.rect_collision.center)

    def update(self):
        # Move the projectile in the direction of the mouse
        self.rect_collision.center += self.direction * self.speed
        self.rect.center = self.rect_collision.center

        self.animate()

        for sprite in self.obstacle_sprites:
            if sprite.rect_collision.colliderect(self.rect_collision):
                if self.attack_type != 'stab':
                    self.kill()

        for sprite in self.damageable_sprites:
            if sprite.rect_collision.colliderect(self.rect_collision):
                if self.attack_type != 'stab':
                    self.kill()

        for sprite in self.destructable_sprites:
            if sprite.rect_collision.colliderect(self.rect_collision):
                sprite.kill()
                if self.attack_type != 'stab':
                    self.kill()

class Melee(Projectile):
    def __init__(self, player, groups, obstacle_sprites, destructable_sprites, damageable_sprites, speed=0, attack_type='stab', player_distance = 100):
        super().__init__(player, groups, obstacle_sprites, destructable_sprites, damageable_sprites, speed, attack_type, player_distance)
        self.duration = 400
        self.attack_time = pygame.time.get_ticks()
        self.animation_speed = 0.3

        self.stab_sound = pygame.mixer.Sound('./audio/sword.wav')
        self.stab_sound.set_volume(0.3)
        self.stab_sound.play()

    def attack_duration(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_time >= self.duration:
            self.kill()

    def rotate_animation(self):
        mouse_angle = degrees(atan2(self.direction.x, self.direction.y))
        if self.direction.x > 0:
            self.image = pygame.transform.rotozoom(self.image_original, (mouse_angle - 135), 1)
            
        else:
            self.image = pygame.transform.rotozoom(self.image_original, ((mouse_angle- 225) * -1), 1)
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        super().update()
        self.rotate_animation()
        self.attack_duration()