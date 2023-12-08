##############################################################################
#                                Import files                                #
##############################################################################
from terrain.lightning.shadow.Shadow import Shadow, Light
from engine_math.functions import get_normal_of_segment


##############################################################################
#                              Import librairies                             #
##############################################################################
import pygame as pg
from pygame import Vector2 as vec2
import math


##############################################################################
#                                    Class                                   #
##############################################################################
class ShadowCircle(Shadow):
    def __init__(
            self,
            position:tuple[float, float],
            radius:float,
        ) -> None:
        """
        position:tuple[float, float] -> the position of the center of the shadow obstacle
        points:list[tuple[float, float]] -> list of point relative of center, need to be in clock wise !
        degree:float=0 -> start rotation in degrees
        """
        # Call parent constructor
        super().__init__(position)

        # Creation lists of points
        self.radius = radius
        self.radius_squarred = self.radius ** 2


    def draw(self, surface:pg.Surface, color:tuple[int, int, int]):
        """
        Method to draw the shadow's shape for debuging
        """
        pg.draw.circle(surface, color, self.position, self.radius)


    def draw_outline(
            self,
            surface:pg.Surface,
            outline_color:tuple[int, int, int]=(0, 255, 0),
            outline_width:int=2
            ):
        """
        Method to draw the outline for debuging
        """
        pg.draw.circle(surface, color, self.position, self.radius, outline_width)


    def draw_shadow(
            self,
            surface:pg.Surface,
            light:Light
        ):
        """
        Method to draw the shadow on the light surface, to change light effect shape
        """
        # Check if light is not too far
        distance_from_light = (light.position - self.position).length_squared()
        if distance_from_light - self.radius_squarred > light.effect_range_squared:
            return

        # Compute values for projection
        position = self.position - light.surface_position
        move_vec = get_normal_of_segment(self.position, light.position) * self.radius
        distance_from_light = math.sqrt(distance_from_light)
        shadow_lenght = light.effect_range - distance_from_light

        # Compute points for projection
        point_1 = position + move_vec
        point_2 = position - move_vec

        # Compute first point projection
        dir_point_1_light = (point_1 - light.position_into_surface).normalize()
        projection_point_1 = point_1 + dir_point_1_light * shadow_lenght

        # Compute second point projection
        dir_point_2_light = (point_2 - light.position_into_surface).normalize()
        projection_point_2 = point_2 + dir_point_2_light * shadow_lenght

        # Draw the shadow
        pg.draw.circle(surface, (0, 0, 0, 0), position, self.radius)
        pg.draw.polygon(surface, (0, 0, 0, 0), [point_1, projection_point_1, projection_point_2, point_2])


    def rotate(self, degrees:float):
        """
        Method to rotate the shadow by degrees
        """
        pass


    def move(self, direction:tuple[float, float] | vec2):
        """
        Method to move the shadow by pass a vector as tupple
        """
        direction = vec2(direction)
        self.position += direction


    def setPosition(self, position:tuple[float, float] | vec2):
        """
        Method to set the shadow position by pass a vector as tupple
        """
        position = vec2(position)
        self.position = position
