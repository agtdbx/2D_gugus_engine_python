from terrain.lightning.lights.Light import Light
from terrain.Segment import Segment

import pygame as pg
from pygame import Vector2 as vec2


class ShadowPolygon:
	def __init__(
			self,
			position:tuple[float, float],
			points:list[tuple[float, float]],
			degree:float=0,
			color:tuple[int, int, int]=(0, 0, 200),
			outline_color:tuple[int, int, int]=(0, 0, 255)
		) -> None:
		"""
		Class to make an

		position:tuple[float, float] -> the position of the center of the shadow obstacle
		points:list[tuple[float, float]] -> list of point relative of center, need to be in clock wise !
		degree:float=0 -> start rotation in degrees
		color:tuple[int, int, int]=(0, 0, 150) -> the color of the polygon
		outline_color:tuple[int, int, int]=(0, 0, 255) -> the color of the polygon's border
		"""
		self.position = vec2(position)
		self.points = []
		self.circle_arround_radius = 0
		for point in points:
			p = vec2(point)
			dist = p.length()
			if dist > self.circle_arround_radius:
				self.circle_arround_radius = dist
			self.points.append(p + self.position)
		self.number_of_points = len(self.points)

		self.circle_arround_radius_squared = self.circle_arround_radius ** 2

		self.color = pg.Color(color)
		self.outline_color = pg.Color(outline_color)

		self.segments = []

		if degree != 0:
			self.rotate(degree)
		else:
			self._compute_segments()


	def draw(self, surface:pg.Surface):
		pg.draw.polygon(surface, self.color, self.points)


	def draw_outline(self, surface:pg.Surface, with_normals:bool=False):
		for segment in self.segments:
			segment.draw(surface)
			if with_normals:
				segment.draw_normal(surface)


	def draw_shadow(
			self,
			surface:pg.Surface,
			light:Light
		):
		# Check if light is not too far
		if (light.position - self.position).length_squared() - self.circle_arround_radius_squared > light.effect_range_squared:
			return
		# Compute all shadow point
		for seg in self.segments:
			shadow_projection = seg.get_shadow_projection(light)
			if shadow_projection != None:
				pg.draw.polygon(surface, (0, 0, 0, 0), shadow_projection)


	def move(self, direction:vec2):
		self.position += direction
		for i in range(self.number_of_points):
			self.points[i] += direction
		self._compute_segments()


	def setPosition(self, position:vec2):
		moveDir = position - self.position
		self.position = position
		for i in range (len(self.points)):
			self.points[i] += moveDir
		self._compute_segments()


	def rotate(self, degrees:float):
		for i in range(self.number_of_points):
			self.points[i] -= self.position
			self.points[i] = self.points[i].rotate(degrees)
			self.points[i] += self.position
		self._compute_segments()


	def _compute_segments(self):
		if self.number_of_points <= 1:
			return
		self.segments.clear()
		for i in range(self.number_of_points):
			start = self.points[i - 1]
			end = self.points[i]
			self.segments.append(Segment(start, end, color=self.outline_color))
