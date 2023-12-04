##############################################################################
#                                Import files                                #
##############################################################################
from terrain.lightning.lights.Light import Light
from engine_math.Segment import Segment


##############################################################################
#                              Import librairies                             #
##############################################################################
import pygame as pg
from pygame import Vector2 as vec2
from abc import ABC, abstractmethod
import math


##############################################################################
#                                 Class Shadow                               #
##############################################################################
class Shadow(ABC):
    def __init__(
            self,
            position:tuple[float, float],
        ) -> None:
        """
        position:tuple[float, float] -> the position of the center of the shadow obstacle
        points:list[tuple[float, float]] -> list of point relative of center, need to be in clock wise !
        degree:float=0 -> start rotation in degrees
        """
        self.position = vec2(position)
        self.circle_arround_radius_squared = 0


    @abstractmethod
    def draw(self, surface:pg.Surface, color:tuple[int, int, int]):
        """
        Method to draw the shadow's shape for debuging
        """
        pass


    @abstractmethod
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
        pass


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


    @abstractmethod
    def move(self, direction:tuple[float, float] | vec2):
        """
        Method to move the shadow by pass a vector as tupple
        """
        pass


    @abstractmethod
    def setPosition(self, position:tuple[float, float] | vec2):
        """
        Method to set the shadow position by pass a vector as tupple
        """
        pass


    @abstractmethod
    def rotate(self, degrees:float):
        """
        Method to rotate the shadow by degrees
        """
        pass


def segment_shadow_projection(
        segment:Segment,
        light:Light) -> list[tuple[vec2, vec2]] | None:
    """
    Calculate the point for create a shadow polygon
    Return None if there is no shadow
    Return the list of tupple of point. Like this :
    [
        (point, point_projected_by_shadow)
    ]
    """
    direction_light_segment = segment.center - light.position
    dist = direction_light_segment.length_squared()
    if dist == 0 or dist > light.effect_range_squared:
        return None
    dist = math.sqrt(dist)
    direction_light_segment /= dist
    # If the light and the normal are in same direction, no shadow
    if direction_light_segment.dot(segment.normal) > 0:
        return None

    start = segment.start_point - light.surface_position
    end = segment.end_point - light.surface_position

    direction_light_start = segment.start_point - light.position
    distance_light_start = direction_light_start.length()
    direction_light_start /= distance_light_start

    direction_light_end = segment.end_point - light.position
    distance_light_end = direction_light_end.length()
    direction_light_end /= distance_light_end

    length_of_projection = light.effect_range - min(distance_light_start, distance_light_end)

    start_projection = start + direction_light_start * length_of_projection
    end_projection = end + direction_light_end * length_of_projection

    return (start, start_projection, end_projection, end)
