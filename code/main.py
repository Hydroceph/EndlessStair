import pygame, sys
from game_data import WIDTH, HEIGHT, FPS
from level import Level

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption('Hydroceph')
		self.clock = pygame.time.Clock()

		# create an instance of the Level Class, which contains all the Sprites
		self.level = Level() 
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_y:
						self.level.toggle_upgrade()
					if event.key == pygame.K_t:
						self.level.dialogue_check()
						print('dialogue main')

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