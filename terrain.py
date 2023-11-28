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
		self.lights.append(Light((500, 500), 300, 150, (255, 0, 0, 255)))
		self.lights.append(Light((650, 450), 200, 200, (0, 255, 0, 255)))
		self.lights.append(Light((600, 350), 150, 250, (0, 0, 255, 255)))

		self.shadow_surface = pg.Surface(self.size, pg.SRCALPHA)
		self.shadow_strengh = 230

		self.shadow_obstacles = []
		self.shadow_obstacles.append(Shadow_obstacle(
			(400, 400),
			[(-20, 20), (0, -20), (20, 20)]
		))
		self.shadow_obstacles.append(Shadow_obstacle(
			(600, 400),
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
		# Apply shadow every where
		self.shadow_surface.fill(shadow_color)

		# Compute lights surface
		self.lights_surface = []
		for light in self.lights:
			# Copy the surface
			surface = self.shadow_surface.copy()
			# Apply the light
			light.draw(surface)
			light.draw_source(surface)
			# Apply the shadows
			for shadow_obstacle in self.shadow_obstacles:
				shadow_obstacle.draw_shadow(surface, shadow_color, light)
			# Save the light_surface
			self.lights_surface.append(surface)

		# Blit all surfaces
		for surface in self.lights_surface:
			self.shadow_surface.blit(surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

