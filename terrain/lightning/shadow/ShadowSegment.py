##############################################################################
#                                Import files                                #
##############################################################################
from terrain.lightning.lights.Light import Light
from engine_math.functions import get_normal_of_segment


##############################################################################
#                              Import librairies                             #
##############################################################################
import pygame as pg
from pygame import Vector2 as vec2
import math


##############################################################################
#                                Class Segment                               #
##############################################################################
class ShadowSegment:
    def __init__(
            self,
            start_point:tuple[float, float],
            end_point:tuple[float, float],
            width:int=2,
        ) -> None:
        self.start_point = vec2(start_point)
        self.end_point = vec2(end_point)
        self.width = width

        self.direction = self.end_point - self.start_point
        self.length = self.direction.length()
        self.normal = get_normal_of_segment(self.start_point, self.end_point)
        self.center = self.start_point + self.direction / 2


    def draw(self, surface:pg.Surface, color:tuple[int, int, int]):
        pg.draw.line(surface, color, self.start_point, self.end_point, self.width)


    def draw_normal(
            self,
            surface:pg.Surface,
            color:tuple[int, int, int]=(255, 0, 0),
            lenght:float=10
        ):
        pg.draw.line(surface, color, self.center, self.center + self.normal * lenght, self.width)


    def get_shadow_projection(self, light:Light) -> list[tuple[vec2, vec2]] | None:
        """
        Calculate the point for create a shadow polygon
        Return None if there is no shadow
        Return the list of tupple of point. Like this :
        [
            (point, point_projected_by_shadow)
        ]
        """
        direction_light_segment = (self.center - light.position)
        dist = direction_light_segment.length_squared()
        if dist == 0 or dist > light.effect_range_squared:
            return None
        dist = math.sqrt(dist)
        direction_light_segment /= dist
        # If the light and the normal are in same direction, no shadow
        if direction_light_segment.dot(self.normal) > 0:
            return None

        start = self.start_point - light.surface_position
        end = self.end_point - light.surface_position

        direction_light_start = self.start_point - light.position
        distance_light_start = direction_light_start.length()
        direction_light_start /= distance_light_start

        direction_light_end = self.end_point - light.position
        distance_light_end = direction_light_end.length()
        direction_light_end /= distance_light_end

        length_of_projection = light.effect_range - min(distance_light_start, distance_light_end)

        start_projection = start + direction_light_start * length_of_projection
        end_projection = end + direction_light_end * length_of_projection

        return (start, start_projection, end_projection, end)

