from terrain import Terrain

import pygame as pg
from pygame import Vector2
import time
import sys
class Game:
	def __init__(self):
		"""
		This method define all variables needed by the program
		"""
		# Start of pygame
		pg.init()

		self.screen_size = Vector2(1920, 1080)
		# We create the window
		self.screen = pg.display.set_mode(self.screen_size, pg.RESIZABLE)

		self.clock = pg.time.Clock() # The clock be used to limit our fps
		self.fps = -1

		self.last = time.time()

		self.run_main_loop = True

		self.terrain = Terrain(self.screen_size, (255, 255, 255, 255))


	def run(self):
		"""
		This method is the main loop of the game
		"""
		# Game loop
		while self.run_main_loop:
			self.input()
			self.tick()
			self.render()
			self.clock.tick(self.fps)


	def input(self):
		"""
		The method catch user's inputs, as key presse or a mouse click
		"""
		# We check each event
		for event in pg.event.get():
			# If the event it a click on the top right cross, we quit the game
			if event.type == pg.QUIT:
				self.quit()

		self.keyboardState = pg.key.get_pressed()
		self.mouseState = pg.mouse.get_pressed()
		self.mousePos = pg.mouse.get_pos()

		# Press espace to quit
		if self.keyboardState[pg.K_ESCAPE]:
			self.quit()


	def tick(self):

		"""
		This is the method where all calculations will be done
		"""
		tmp = time.time()
		delta = tmp - self.last
		self.last = tmp

		self.terrain.update(delta)

		pg.display.set_caption(str(self.clock.get_fps()))


	def render(self):
		"""
		This is the method where all graphic update will be done
		"""
		# We clean our screen with one color
		self.screen.fill((0, 0, 0))
		self.terrain.draw(self.screen)
		pg.display.flip()


	def quit(self):
		"""
		This is the quit method
		"""
		# Pygame quit
		pg.quit()
		sys.exit()

if __name__ == '__main__':
	Game().run() # Start game
