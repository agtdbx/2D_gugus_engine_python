from light import Light

import pygame as pg
from pygame import Vector2


class Segment:
	def __init__(
			self,
			start_point:tuple[float, float],
			end_point:tuple[float, float],
			width:int=2,
			color:tuple[int, int, int]=(0, 0, 255)
		) -> None:
		self.start_point = Vector2(start_point)
		self.end_point = Vector2(end_point)
		self.width = width
		self.color = pg.Color(color)

		self.direction = self.end_point - self.start_point
		self.length = self.direction.length()
		self.normal = get_normal_of_segment(self.start_point, self.end_point)
		self.center = self.start_point + self.direction / 2


	def draw(self, surface:pg.Surface):
		pg.draw.line(surface, self.color, self.start_point, self.end_point, self.width)


	def draw_normal(
			self,
			surface:pg.Surface,
			color:tuple[int, int, int]=(255, 0, 0),
			lenght:float=10
		):
		pg.draw.line(surface, color, self.center, self.center + self.normal * lenght, self.width)


	def get_shadow_projection(self, light:Light) -> list[tuple[Vector2, Vector2]] | None:
		"""
		Calculate the point for create a shadow polygon
		Return None if there is no shadow
		Return the list of tupple of point. Like this :
		[
			(point, point_projected_by_shadow)
		]
		"""
		direction_light_segment = (self.center - light.position).normalize()
		# If the light and the normal are in same direction, no shadow
		if direction_light_segment.dot(self.normal) > 0:
			return None

		direction_light_start = self.start_point - light.position
		distance_light_start = direction_light_start.length()

		direction_light_end = self.end_point - light.position
		distance_light_end = direction_light_end.length()

		# If both point arent in the light range
		if distance_light_start > light.total_range and distance_light_end > light.total_range:
			return None
		direction_light_start /= distance_light_start
		direction_light_end /= distance_light_end

		length_of_projection = light.total_range - min(distance_light_start, distance_light_end)

		start_projection = self.start_point + direction_light_start * length_of_projection
		end_projection = self.end_point + direction_light_end * length_of_projection

		return [(self.start_point.copy(), start_projection), (self.end_point.copy(), end_projection)]


def get_normal_of_segment(start:Vector2, end:Vector2) -> Vector2:
	dx = end.x - start.x
	dy = end.y - start.y
	vec = Vector2(-dy, dx)
	return vec.normalize() * -1
