
"""wasd to move, left shift and spacebar for damage, t to start dialogue, g to continue dialogue, y to open upgrade menu, h to start etc."""

import pygame, sys
from game_data import WIDTH, HEIGHT, FPS
from level import Level
from game_data import FONT, png_collection

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption('Hydroceph')
		self.clock = pygame.time.Clock()

		# start and death screen graphic variables
		font = pygame.font.Font(FONT, 50)
		self.frame_index = 0
		self.animation_speed = 0.15

		# background music
		bg_music = pygame.mixer.Sound('./audio/soundtrack/Fastest Spook.wav')
		bg_music.set_volume(0.5)
		bg_music.play(loops = -1)

		# start screen
		self.start_message = font.render('Press H to start', False, 'yellow')
		self.start_message_rect = self.start_message.get_rect(center = (640, 500))
		self.start_flame_list = png_collection('./graphics/particles/flame/frames')
		self.start_flame = pygame.image.load('./graphics/particles/flame/frames/0.png')
		self.start_flame_rect = self.start_flame.get_rect(center = (640, 300))

		# death screen
		self.death_message = font.render('Press H to try again', False, 'yellow')
		self.death_message_rect = self.death_message.get_rect(center = (640, 500))
		self.dead_player = pygame.image.load('./graphics/underworld/Heroes/Wizzard/Death/collection/Wiz_death_6.png')
		self.dead_player = pygame.transform.scale_by(self.dead_player, 3)
		self.dead_player_rect = self.dead_player.get_rect(center = (640, 300))
		# create an instance of the Level Class, which contains all the Sprites
		self.level = Level() 
	
	def animate_flame(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.start_flame_list) - 1e-6:
			self.frame_index = 0
		self.start_flame = self.start_flame_list[int(self.frame_index)]
		self.start_flame = pygame.transform.scale_by(self.start_flame, 3)

		self.start_flame_rect = self.start_flame.get_rect(center = (640,300))

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_y:
						self.level.toggle_upgrade()
					elif event.key == pygame.K_t:
						self.level.dialogue_check()
					elif event.key == pygame.K_h:
						if self.level.game_state == 'start':
							self.level.game_state = 'running'
						elif self.level.game_state == 'dead':
							self.level = Level()

			if self.level.game_state == 'start':
				self.screen.fill((0,0,0))
				self.screen.blit(self.start_message, self.start_message_rect)
				self.animate_flame()
				self.screen.blit(self.start_flame, self.start_flame_rect)
			elif self.level.game_state == 'dead':
				self.screen.fill((0,0,0))
				self.screen.blit(self.death_message, self.death_message_rect)
				self.screen.blit(self.dead_player, self.dead_player_rect)
			else:
				self.screen.fill('black')
				# draw and update everything in Level
				self.level.run() 

			# update and display onto the actual screen
			pygame.display.update()
			# set max framerate
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()