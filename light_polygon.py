import pygame as pg
from pygame import Vector2


class Light_polygon:
	def __init__(
			self,
			position:tuple[int, int],
			points:list[tuple[int, int]],
			range:float,
			range_full_power:float,
			power:int,
			color:tuple[int, int, int],
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

		self.points = []
		min_x = 0
		max_x = 0
		min_y = 0
		max_y = 0
		max_lenght = 0
		for p in points:
			point = Vector2(p)
			if point.x < min_x:
				min_x = point.x
			if point.x > max_x:
				max_x = point.x
			if point.y < min_y:
				min_y = point.y
			if point.y > max_y:
				max_y = point.y
			lenght = point.length()
			if lenght > max_lenght:
				max_lenght = lenght
			self.points.append(point)

		for point in self.points:
			point /= max_lenght

		min_x /= max_lenght
		max_x /= max_lenght
		min_y /= max_lenght
		max_y /= max_lenght

		self.range = range
		self.power = power
		self.color = pg.Color(color)
		self.range_full_power = range_full_power
		self.radial_smooth_precision = radial_smooth_precision

		if self.radial_smooth_precision > self.range:
			self.radial_smooth_precision = self.range

		self.total_range = self.range + self.range_full_power

		min_x *= self.total_range
		max_x *= self.total_range
		min_y *= self.total_range
		max_y *= self.total_range

		self.surface_size = Vector2(max_x - min_x + 1, max_y - min_y + 1)
		self.surface = pg.Surface(self.surface_size, pg.SRCALPHA)
		self.surface_position = self.position - (self.surface_size / 2)

		self.center = Vector2(-min_x, -min_y)

		self._compute_light_surface()


	def draw(self, light_surface:pg.Surface):
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

		points = []

		# Draw the full power polygon if necessary
		if self.range_full_power > 0:
			for point in self.points:
				p = point.copy()
				p *= self.range_full_power
				p += self.center
				points.append(p)
			pg.draw.polygon(self.surface, color, points)
			size += self.range_full_power

		# Draw the light smouth
		for _ in range(self.radial_smooth_precision):
			points.clear()
			for point in self.points:
				p = point.copy()
				p *= size
				p += self.center
				points.append(p)
			pg.draw.polygon(self.surface, color, points, int(width * 2))
			size += width
			color[3] -= decrease_alpha
