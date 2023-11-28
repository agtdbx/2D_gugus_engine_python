from light import Light
from shadow_polygon import Shadow_polygon

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
			self.lights_surface.append(self.lights[i].surface.copy())

		self.shadow_surface = pg.Surface(self.size, pg.SRCALPHA)
		self.shadow_strengh = 230

		self.shadow_polygons = []
		for y in range(50, int(self.size.y), 100):
			for x in range(50, int(self.size.x), 100):
				self.shadow_polygons.append(Shadow_polygon(
					(x, y),
					[(-30, 10), (-30, -10), (-20, -10), (-20, 0), (20, 0), (20, -10), (30, -10), (30, 10)]
				))
				#self.shadow_polygons.append(Shadow_polygon(
				#	(x, y),
				#	[(-10, -20), (10, -20), (10, 20), (-10, 20)]
				#))


	def update(self, delta):
		for shadow_polygon in self.shadow_polygons:
			shadow_polygon.rotate(45 * delta)
		self._updateDraw()


	def draw(self, screen:pg.Surface):
		screen.blit(self.surface, (0, 0))


	def _updateDraw(self):
		self.surface.fill(self.background_color)

		# Draw all terrain
		for shadow_polygon in self.shadow_polygons:
			shadow_polygon.draw(self.surface)

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
			# self.lights_surface[i] = self.lights[i].surface.copy()

			self.lights_surface[i].fill(shadow_color)
			# Apply the light
			self.lights[i].draw(self.lights_surface[i])
			# Apply the shadows
			for shadow_polygon in self.shadow_polygons:
				shadow_polygon.draw_shadow(self.lights_surface[i], self.lights[i])

		# Blit all surfaces
		blit_list = []
		for i in range(len(self.lights_surface)):
			blit_list.append((self.lights_surface[i], self.lights[i].surface_position, None, pg.BLEND_RGBA_MAX))

		self.shadow_surface.blits(blit_list)

