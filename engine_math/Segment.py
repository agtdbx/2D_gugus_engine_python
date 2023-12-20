##############################################################################
#                              Import librairies                             #
##############################################################################
import pygame as pg
from pygame import Vector2 as vec2
import math


##############################################################################
#                                Class Segment                               #
##############################################################################
class Segment:
    def __init__(
            self,
            start_point:tuple[float, float],
            end_point:tuple[float, float]
        ) -> None:
        self.start_point = vec2(start_point)
        self.end_point = vec2(end_point)
        self._compute_variables()


    def _compute_variables(self):
        self.vec2 = self.end_point - self.start_point
        self.direction = self.vec2.copy()
        self.length = self.direction.length()
        if self.length > 0:
            self.direction /= self.length
        self.center = self.start_point + self.direction / 2
        # Normal calculation
        self._compute_normal()


    def _compute_normal(self):
        dx = self.end_point.x - self.start_point.x
        dy = self.end_point.y - self.start_point.y
        if dx == 0 and dy == 0:
            self.normal = vec2(0, 0)
        vec = vec2(-dy, dx)
        self.normal = vec.normalize() * -1


    def set_start_point(self, start_point:tuple[float, float] | vec2):
        self.start_point = start_point
        self._compute_variables()


    def set_end_point(self, end_point:tuple[float, float] | vec2):
        self.end_point = end_point
        self._compute_variables()


    def set_direction(self, direction:vec2):
        self.direction = direction
        self.end_point = self.start_point + self.direction * self.length
        self._compute_normal()


    def modify_direction(self, direction:vec2):
        self.direction += direction
        self.direction.normalize()
        self.end_point = self.start_point + self.direction * self.length
        self._compute_normal()


    def move(self, direction:vec2):
        self.start_point += direction
        self.end_point += direction
        self._compute_variables()


    def draw(self, surface:pg.Surface, color:tuple[int, int, int], width:int=2):
        pg.draw.line(surface, color, self.start_point, self.end_point, width)


    def draw_normal(
            self,
            surface:pg.Surface,
            color:tuple[int, int, int]=(255, 0, 0),
            lenght:float=10,
            width:int=2
        ):
        pg.draw.line(surface, color, self.center, self.center + self.normal * lenght, width)


    def collide_with_segment(
            self,
            seg_point_start:vec2,
            seg_point_end:vec2) -> tuple[bool, vec2]:
        """
        Calculate the point of the intersection beetween
        Return None if there is no shadow
        Return the list of tupple of point. Like this :
        [
            (point, point_projected_by_shadow)
        ]
        """
        divisor = (self.start_point.x - self.end_point.x) * (seg_point_start.y - seg_point_end.y) - (self.start_point.y - self.end_point.y) * (seg_point_start.x - seg_point_end.x)
        if divisor == 0:
            return False, None

        t = (self.start_point.x - seg_point_start.x) * (seg_point_start.y - seg_point_end.y) - (self.start_point.y - seg_point_start.y) * (seg_point_start.x - seg_point_end.x)
        t /= divisor

        if t < 0 or 1 < t:
            return False, None

        u = (self.start_point.x - seg_point_start.x) * (self.start_point.y - self.end_point.y) - (self.start_point.y - seg_point_start.y) * (self.start_point.x - self.end_point.x)
        u /= divisor

        if u < 0 or 1 < u:
            return False, None

        # Point of intersection
        s1Dir = self.end_point - self.start_point
        p = self.start_point + s1Dir * t

        return True, p
