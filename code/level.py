
""" Class which handles the drawing, updating and interaction between all the sprite groups """

import pygame 
from map import TILESIZE, dung_room_0_layout, dung_room_0_graphics
from prop import Prop
from player import Player
from debug import debug

class Level:
	def __init__(self):

		""" Sprite Groups """
		self.visible_sprites = Camera()
		self.obstacle_sprites = pygame.sprite.Group()

		self.create_map()

	# create sprites based on map in settings
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
							self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)
						if layer == 'pillars':
							surface = dung_tiles_list[int(col)]
							Prop((x,y),[self.visible_sprites,self.obstacle_sprites], surface)
		

	# update and draw everything. Custom draw method to allow camera offset
	def run(self):
		self.visible_sprites.offset_draw(self.player)
		self.visible_sprites.update()

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

		# create floor seperately as image, so it is always on bottom (and does not interact with the y sort)
		self.floor_surface = pygame.image.load('./map/dungeon/room_0/dung_room_0_floor.png')
		self.floor_surface = pygame.transform.scale_by(self.floor_surface, 4)
		self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

	def offset_draw(self, player):
		# find player distance from midpoint of screen
		self.offset.x = player.rect.centerx - self.midpoint_x
		self.offset.y = player.rect.centery - self.midpoint_y

		# drawing the floor
		floor_offset_fix = pygame.math.Vector2(32,32)
		floor_offset = self.floor_rect.topleft - self.offset + floor_offset_fix
		self.display_surface.blit(self.floor_surface, floor_offset)

		# make new sprite rectangle to blit image onto, which will be in different position based on offset above
		for sprite in sorted(self.sprites(), key = self.y_sort):
			sprite_offset = sprite.rect.center - self.offset
			self.display_surface.blit(sprite.image, sprite_offset)

	def y_sort(self, to_sort):
		return to_sort.rect.centery
	