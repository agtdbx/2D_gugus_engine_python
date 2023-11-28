import pygame as pg
from pygame import Vector2


class Light:
	def __init__(
			self,
			position:tuple[int, int],
			range:float,
			power:int,
			color:tuple[int, int, int],
			range_full_power:float=0,
			radial_smooth_precision:int=100
		) -> None:
		"""
		position:tuple[int, int] -> Center of the light, in pixel (Become Vector2)
		range:float -> Radius of the light effect, in pixel
		power:int -> Power of the light, [1, 255]
		color:tuple[int, int, int] -> Color of the light
		range_full_power:float -> Radius of a circle with full power of the light
		radial_smooth_precision:int -> The precision of the light. More it is, more gradient you will have
		"""
		self.position = Vector2(position)
		self.range = range
		self.power = power
		self.color = pg.Color(color)
		self.range_full_power = range_full_power
		self.radial_smooth_precision = radial_smooth_precision

		self.total_range = self.range + self.range_full_power

		self.surface_size = Vector2((self.range + self.range_full_power) * 2, (self.range + self.range_full_power) * 2)
		self.surface = pg.Surface(self.surface_size, pg.SRCALPHA)
		self.surface_position = self.position - (self.surface_size / 2)
		self._compute_light_surface()

	def draw(self, light_surface:pg.Surface):
		# light_surface.blit(self.surface, self.surface_position)
		light_surface.blit(self.surface, (0, 0))

	def draw_source(self, light_surface:pg.Surface):
		if self.range_full_power > 0:
			pg.draw.circle(light_surface, self.color, self.position, self.range_full_power)
		else:
			pg.draw.circle(light_surface, self.color, self.position, 1)


	def _compute_light_surface(self):
		# Compute some variable for draw smouth light
		color = [self.color.r, self.color.g, self.color.b, self.power]
		decrease_alpha = self.power / self.radial_smooth_precision
		width = self.range / self.radial_smooth_precision
		size = width

		# Draw the full power circle if necessary
		if self.range_full_power > 0:
			pg.draw.circle(self.surface, color, self.surface_size / 2, self.range_full_power)
			size += self.range_full_power

		# Draw the light smouth
		for _ in range(self.radial_smooth_precision):
			pg.draw.circle(self.surface, color, self.surface_size / 2, size, int(width * 2))
			size += width
			color[3] -= decrease_alpha
