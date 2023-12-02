##############################################################################
#                                Import files                                #
##############################################################################
from terrain.lightning.lights.Light import Light
from terrain.Segment import Segment


##############################################################################
#                              Import librairies                             #
##############################################################################
import pygame as pg
from pygame import Vector2 as vec2
from abc import ABC, abstractmethod


##############################################################################
#                                 Class Shadow                               #
##############################################################################
class Shadow(ABC):
    def __init__(
            self,
            position:tuple[float, float],
            points:list[tuple[float, float]],
            degree:float=0,
        ) -> None:
        """
        position:tuple[float, float] -> the position of the center of the shadow obstacle
        points:list[tuple[float, float]] -> list of point relative of center, need to be in clock wise !
        degree:float=0 -> start rotation in degrees
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

        self.segments = []

        if degree != 0:
            self.rotate(degree)
        else:
            self._compute_segments()


    @abstractmethod
    def draw(self, surface:pg.Surface, color:tuple[int, int, int]):
        """
        Method to draw the shadow's shape for debuging
        """
        pass


    def draw_outline(
            self,
            surface:pg.Surface,
            with_normals:bool=False,
            segment_color:tuple[int, int, int]=(0, 255, 0),
            normal_color:tuple[int, int, int]=(255, 0, 0)
        ):
        """
        Method to draw the outline for debuging
        """
        for segment in self.segments:
            segment.draw(surface, segment_color)
            if with_normals:
                segment.draw_normal(surface, normal_color)


    @abstractmethod
    def draw_shadow(
            self,
            surface:pg.Surface,
            light:Light
        ):
        """
        Method to draw the shadow on the light surface, to change light effect shape
        """
        pass


    def move(self, direction:tuple[float, float] | vec2):
        """
        Method to move the shadow by pass a vector as tupple
        """
        direction = vec2(direction)
        self.position += direction
        for i in range(self.number_of_points):
            self.points[i] += direction
        self._compute_segments()


    def setPosition(self, position:tuple[float, float] | vec2):
        """
        Method to set the shadow position by pass a vector as tupple
        """
        position = vec2(position)
        moveDir = position - self.position
        self.position = position
        for i in range (len(self.points)):
            self.points[i] += moveDir
        self._compute_segments()


    def rotate(self, degrees:float):
        """
        Method to rotate the shadow by degrees
        """
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
            self.segments.append(Segment(start, end))
