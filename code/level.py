
""" Class which handles the drawing, updating and interaction between all the sprite groups """

import pygame 
from graphics import TILESIZE, WIDTH, HEIGHT, FOG_COLOUR, dung_room_0_layout, dung_room_0_graphics
from npc import Prop, Projectile, Melee, Enemy, PatrolEnemy, StaticWeapon, CQCWeapon, EnemyProjectile
from player import Player
from debug import debug
from gui import GUI

class Level:
	def __init__(self):

		""" Sprite Groups """
		self.visible_sprites = Camera()
		self.obstacle_sprites = pygame.sprite.Group()
		self.destructable_sprites = pygame.sprite.Group()
		self.constraints_sprites = pygame.sprite.Group()
		self.damage_sprites = pygame.sprite.Group()
		self.damageable_sprites = pygame.sprite.Group()

		# create spries based on tiled csv
		self.create_map()

		# GUI
		self.gui = GUI()

	# create sprites based on map from tiled
	def create_map(self):
		layout = dung_room_0_layout # use this to add extra different map levels later?
		dung_tiles_list = dung_room_0_graphics["dung_tiles"]
		dung_props_list = dung_room_0_graphics["dung_props"]
		spawns_list = dung_room_0_graphics["spawns"]

		for layer, map in layout.items():
			for row_index,row in enumerate(map):
				for col_index, col in enumerate(row):
					if col != '-1': # this is empty/blank space
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if layer == 'player':
							self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites, self.create_projectile, self.create_melee)
							self.static_weapon = StaticWeapon(self.player, self.visible_sprites, 'staff')
							self.cqc_weapon = CQCWeapon(self.player, self.visible_sprites, 'sword')
						elif layer == 'pillars':
							surface = dung_tiles_list[int(col)]
							Prop((x,y),[self.visible_sprites,self.obstacle_sprites], surface, -16, -42)
						elif layer == 'invis_walls': # underneath the lighing
							surface = dung_tiles_list[int(col)]
							Prop((x,y),[self.obstacle_sprites], surface, -16, -42)
						elif layer == 'back_props_des': # destroyed versions of background props
							surface = dung_props_list[int(col)]
							Prop((x,y),[self.visible_sprites,self.obstacle_sprites], surface, -32, -54)
						elif layer == 'back_props_1':
							surface = dung_props_list[int(col)]
							Prop((x,y),[self.visible_sprites,self.obstacle_sprites, self.destructable_sprites], surface, -32)
						elif layer == 'back_props_2': # the half blocks (like tops of barrels, tables that are visually not the whole tile)
							surface = dung_props_list[int(col)]
							Prop((x,y),[self.visible_sprites,self.obstacle_sprites, self.destructable_sprites], surface, -32, -54)
						elif layer == 'interact':
							surface = dung_props_list[int(col)]
							Prop((x,y),[self.visible_sprites], surface)
						elif layer == 'exit_1':
							surface = dung_tiles_list[int(col)]
							Prop((x,y),[self.visible_sprites], surface)
						elif layer == 'exit_2':
							surface = dung_tiles_list[int(col)]
							Prop((x,y),[self.visible_sprites,self.obstacle_sprites], surface)
						elif layer == 'constraints':
							surface = spawns_list[0]
							Prop((x,y),[self.constraints_sprites], surface)
						elif layer == 'mob':
							if col == '1':
								Enemy([self.visible_sprites, self.damageable_sprites],self.obstacle_sprites, 'orc', (x,y), self.damage_player)
							if col == '2':
								PatrolEnemy([self.visible_sprites, self.damageable_sprites],self.obstacle_sprites, 'skel_mage', (x,y), self.damage_player, self.constraints_sprites, 'horizontal', self.create_enemy_projectile)
							if col == '4':
								PatrolEnemy([self.visible_sprites, self.damageable_sprites],self.obstacle_sprites, 'skel_mage', (x,y), self.damage_player, self.constraints_sprites, 'vertical', self.create_enemy_projectile)

						

	# player attack
	def create_projectile(self):
		Projectile(self.player,[self.visible_sprites, self.damage_sprites], self.obstacle_sprites, self.destructable_sprites, self.damageable_sprites)

	def create_melee(self):
		Melee(self.player,[self.visible_sprites, self.damage_sprites], self.obstacle_sprites, self.destructable_sprites, self.damageable_sprites)

	def player_attack(self):
		if self.damage_sprites:
			for damage_sprite in self.damage_sprites:
				damaged_sprites = pygame.sprite.spritecollide(damage_sprite, self.damageable_sprites, False)
				if damaged_sprites:
					for damaged_sprite in damaged_sprites:
						damaged_sprite.get_damage(self.player, 'magic')

	# enemy attack

	def create_enemy_projectile(self, enemy_source):
		EnemyProjectile(self.player,[self.visible_sprites], self.obstacle_sprites, self.destructable_sprites, enemy_source, self.damage_player)

	def damage_player(self, damage_amount):
		if self.player.player_can_be_hit:
			self.player.health -= damage_amount
			self.player.player_can_be_hit = False
			self.player.last_hit_time = pygame.time.get_ticks()

	# update and draw everything. Custom draw method to allow camera offset
	def run(self):
		self.visible_sprites.offset_draw(self.player)
		self.visible_sprites.update()
		self.visible_sprites.enemy_update(self.player)
		self.player_attack()
		self.gui.display(self.player)

# Finds the vector distance of the player from the centre point of the window, and takes that offset away from each sprite so player stays central in camera
# also adds y sorting of sprites, so the sprite that is below is in front (allows player to stand behind or in front of props)
class Camera(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		# find midpoint of screen
		self.display_surface = pygame.display.get_surface()
		self.midpoint_x = self.display_surface.get_size()[0] // 2
		self.midpoint_y = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# create floor, light seperately as image, so it is always on bottom (and does not interact with the y sort)
		self.floor_surface = pygame.image.load('./map/dungeon/room_0/dung_room_0_floor.png')
		self.floor_surface = pygame.transform.scale(self.floor_surface, (self.floor_surface.get_width() * 4, self.floor_surface.get_height() * 4))
		self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

		self.floor_light_surface = pygame.image.load('./map/dungeon/room_0/dung_room_0_light.png')
		self.floor_light_surface = pygame.transform.scale(self.floor_light_surface, (self.floor_light_surface.get_width() * 4, self.floor_light_surface.get_height() * 4))
		self.floor_light_surface_alpha = 150
		self.floor_light_rect = self.floor_light_surface.get_rect(topleft = (0,0))
		self.floor_light_alpha_check = 1

		# FOW lighting effect
		self.fow_surf = pygame.Surface((WIDTH,HEIGHT))
		self.fow_surf.fill((FOG_COLOUR))
		self.fow_light_surf = pygame.image.load('./map/dungeon/FOW_light.png').convert_alpha()
		self.fow_light_surf = pygame.transform.scale(self.fow_light_surf, (500,500))
		self.fow_light_rect = self.fow_light_surf.get_rect()
		self.fow_light_rect.center = (self.midpoint_x, self.midpoint_y)
		self.fow_surf.blit(self.fow_light_surf, self.fow_light_rect)
		self.fog = 1

	def offset_draw(self, player):
		# find player distance from midpoint of screen
		self.offset.x = player.rect.centerx - self.midpoint_x
		self.offset.y = player.rect.centery - self.midpoint_y

		# Fixes for all inflated sprites to be drawn in proper place, general sprites and then player (different offset required for each value of scale_by)
		offset_fix = pygame.math.Vector2(32,32)
		player_offset_fix = pygame.math.Vector2(16,16)

		# drawing the floor
		floor_offset = self.floor_rect.topleft - self.offset 
		self.display_surface.blit(self.floor_surface, floor_offset)

		# drawing the floor light, with flashing light
		if self.floor_light_surface_alpha <= 130:
			self.floor_light_surface_alpha = 130
			self.floor_light_alpha_check = 1
		elif self.floor_light_surface_alpha >= 255:
			self.floor_light_surface_alpha = 255
			self.floor_light_alpha_check = 0

		if self.floor_light_alpha_check == 1:
			self.floor_light_surface_alpha += 5
		else:
			self.floor_light_surface_alpha -= 5

		self.floor_light_surface.set_alpha(self.floor_light_surface_alpha)
		floor_light_offset = self.floor_light_rect.topleft - self.offset 
		self.display_surface.blit(self.floor_light_surface, floor_light_offset)

		# make new sprite rectangle to blit image onto, which will be in different position based on offset above

		for sprite in sorted(self.sprites(), key = self.y_sort):
			if isinstance(sprite, Player):
				sprite_offset = sprite.rect.center - self.offset - offset_fix - player_offset_fix
			elif isinstance(sprite, Enemy):
				sprite_offset = sprite.rect.center - self.offset - offset_fix - player_offset_fix
			else:
				sprite_offset = sprite.rect.center - self.offset - offset_fix
			self.display_surface.blit(sprite.image, sprite_offset)

			# test_surface = pygame.Surface(sprite.rect.size)
			# BLACK = (0,0,0)
			# test_surface.fill(BLACK)
			# self.display_surface.blit(test_surface, sprite_offset)

		# drawing the FOW
		if self.fog == 1:
			self.display_surface.blit(self.fow_surf, (0,0), special_flags = pygame.BLEND_MULT)
	
	# so that you're not passing player into every single sprite, which is why you have all this seperately
	def enemy_update(self, player):
		enemy_sprites = []
		for sprite in self.sprites():
			if isinstance(sprite, Enemy):
				enemy_sprites.append(sprite)
		for enemy in enemy_sprites:
			enemy.enemy_update(player)

	def y_sort(self, to_sort):
		return to_sort.rect.centery
	