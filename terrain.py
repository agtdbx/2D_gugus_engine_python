from light import Light
from shadow_obstacle import Shadow_obstacle

import pygame as pg
from pygame import Vector2


class Terrain:
	def __init__(
			self,
			size:tuple[int, int],
			background_color:tuple[int, int, int, int]
	) -> None:
		self.size = Vector2(size)
		self.background_color = background_color

		self.surface = pg.Surface(self.size, pg.SRCALPHA)

		self.lights = []

		self.lights.append(Light((320, 300), 400, 200, (255, 0, 0, 255)))
		self.lights.append(Light((960, 300), 400, 200, (0, 255, 0, 255)))
		self.lights.append(Light((1600, 300), 400, 200, (0, 0, 255, 255)))

		self.lights.append(Light((320, 810), 400, 200, (255, 255, 0, 255)))
		self.lights.append(Light((960, 810), 400, 200, (0, 255, 255, 255)))
		self.lights.append(Light((1600, 810), 400, 200, (255, 0, 255, 255)))

		self.lights_surface = []
		for i in range(len(self.lights)):
			self.lights_surface.append(pg.Surface(self.lights[i].surface_size, pg.SRCALPHA))

		self.shadow_surface = pg.Surface(self.size, pg.SRCALPHA)
		self.shadow_strengh = 230

		self.shadow_obstacles = []
		for y in range(50, int(self.size.y), 100):
			for x in range(50, int(self.size.x), 100):
				self.shadow_obstacles.append(Shadow_obstacle(
					(x, y),
					[(-30, 10), (-30, -10), (-20, -10), (-20, 0), (20, 0), (20, -10), (30, -10), (30, 10)]
				))


	def update(self, delta):
		for shadow_obstacle in self.shadow_obstacles:
			shadow_obstacle.rotate(45 * delta)
		self._updateDraw()


	def draw(self, screen:pg.Surface):
		screen.blit(self.surface, (0, 0))


	def _updateDraw(self):
		self.surface.fill(self.background_color)

		# Draw all terrain
		for shadow_obstacle in self.shadow_obstacles:
			shadow_obstacle.draw(self.surface)

		# Draw shadows
		self._compute_light_and_shadow()
		self.surface.blit(self.shadow_surface, (0, 0))


	def _compute_light_and_shadow(self):
		shadow_color = (0, 0, 0, self.shadow_strengh)
		shadow_rect = (0, 0, self.size.x, self.size.y)
		# Apply shadow every where
		pg.draw.rect(self.shadow_surface, shadow_color, shadow_rect)

		# Compute lights surface
		for i in range(len(self.lights)):
			self.lights_surface[i].fill(shadow_color)

			# Apply the light
			self.lights[i].draw(self.lights_surface[i])
			# Apply the shadows
			for shadow_obstacle in self.shadow_obstacles:
				shadow_obstacle.draw_shadow(self.lights_surface[i], self.lights[i])

		# Blit all surfaces
		for i in range(len(self.lights_surface)):
			self.shadow_surface.blit(self.lights_surface[i], self.lights[i].surface_position, special_flags=pg.BLEND_RGBA_MAX)

