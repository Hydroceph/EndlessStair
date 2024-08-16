
""" NPC sprites: props and spawn room guide """

import pygame
from game_data import TILESIZE
from character import Character
from game_data import png_collection

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
        

# NPC that greets player in the spawn room
class Guide(Character):
	def __init__(self, groups, obstacle_sprites, pos):
		super().__init__(groups)

		self.speed = 6
		self.obstacle_sprites = obstacle_sprites

		self.image_list = png_collection('./graphics/underworld/Heroes/Wizzard/Idle/collection')
		self.image = self.image_list[self.frame_index]
		self.image = pygame.transform.scale_by(self.image, 3)

		self.rect = self.image.get_rect(topleft = pos)
		self.rect_collision = self.rect.inflate(-8, -16)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.image_list) - 1e-6:
			self.frame_index = 0
		self.image = self.image_list[int(self.frame_index)]
		self.image = pygame.transform.scale_by(self.image, 3)

		self.rect = self.image.get_rect(center = self.rect_collision.center)

	def update(self):
		self.move(self.speed)
		self.animate()


def check_dialogue_connection(player, npc_to_check, radius = 100, tolerance = 30):
	relative_position = pygame.math.Vector2(npc_to_check.rect.center) - pygame.math.Vector2(player.rect.center)
	if relative_position.length() < radius: # if within the radius
		if relative_position.x < 0: # if player is to the right of guide
			if abs(relative_position.y) < tolerance: # if player is within reasonable y value of guide
				return True
			
class DialogueTree:
	def __init__(self, npc, player, visible_sprites, font, font_size):
		self.npc = npc
		self.player = player
		self.visible_sprites = visible_sprites
		self.font = pygame.font.Font(font, font_size)
		self.font_size = font_size

		self.guide_dialogue = ['go down that trapdoor', 'good luck!']
		self.dialogue_index = 0

		self.current_dialogue = DialogueSprite(self.guide_dialogue[self.dialogue_index], self.npc, self.visible_sprites, self.font)

		self.last_input_time = pygame.time.get_ticks()
		self.key_can_be_pressed = True

	def input(self):
		keys = pygame.key.get_pressed()

		if self.key_can_be_pressed:
			if keys[pygame.K_g]:
				print('hello')
				self.current_dialogue.kill()

				self.dialogue_index += 1
				if self.dialogue_index >= 2: # end dialogue
					self.player.unblock()
				else:
					self.current_dialogue = DialogueSprite(self.guide_dialogue[self.dialogue_index], self.npc, self.visible_sprites, self.font)
				self.key_can_be_pressed = False
				self.last_input_time = pygame.time.get_ticks()


		current_time = pygame.time.get_ticks()
		if current_time - self.last_input_time >= 1000:
			self.key_can_be_pressed = True

	def update(self):
		self.input()
			


class DialogueSprite(pygame.sprite.Sprite):
	def __init__(self, message, npc, groups, font):
		super().__init__(groups)

		text_surface = font.render(message, False, 'yellow')
		background_width = text_surface.get_width() + 10
		background_height = text_surface.get_height() + 10

		background_surface = pygame.Surface((background_width, background_height))
		background_surface.fill('#444444')
		background_surface.blit(text_surface, text_surface.get_rect(center = (background_width /2, background_height / 2)))

		self.image = background_surface
		self.rect = self.image.get_rect(midbottom = npc.rect.midtop)