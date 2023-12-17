##############################################################################
#                                Import files                                #
##############################################################################
from terrain.lightning.shadow.Shadow import Shadow, Light
from engine_math.functions import get_normal_of_segment
from engine_math.Segment import Segment


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
            shadowOnObject:bool=True
        ) -> None:
        """
        position:tuple[float, float] -> the position of the center of the shadow obstacle
        points:list[tuple[float, float]] -> list of point relative of center, need to be in clock wise !
        degree:float=0 -> start rotation in degrees
        shadowOnObject:bool -> If the shadow cover the object. True by default (False is less optimized)
        """
        # Call parent constructor
        super().__init__(position, shadowOnObject)

        # Creation lists of points
        self.radius = radius
        self.radius_squarred = self.radius ** 2
        self.diameter = self.radius * 2


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
        pg.draw.circle(surface, outline_color, self.position, self.radius, outline_width)


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
        normal = get_normal_of_segment(self.position, light.position)
        move_vec = normal * self.radius
        distance_from_light = math.sqrt(distance_from_light)
        shadow_lenght = light.effect_range - distance_from_light
        # Compute points for projection
        point_right = position + move_vec
        point_left = position - move_vec

        # In case of hard shadow only
        if light.inner <= 1:
            # Compute left point projection
            dir_point_left_light = (point_left - light.position_into_surface).normalize()
            projection_point_left = point_left + dir_point_left_light * shadow_lenght

            # Compute right point projection
            dir_point_right_light = (point_right - light.position_into_surface).normalize()
            projection_point_right = point_right + dir_point_right_light * shadow_lenght

            # Creation shadow_points
            shadow_projection = [
                None,
                (point_left, projection_point_left),
                (point_right, projection_point_right),
                None
            ]

        # In case of soft shadow
        else:
            left_light_pos = light.position_into_surface - normal * light.inner
            right_light_pos = light.position_into_surface + normal * light.inner

            # Compute left points projection
            dir_point_left_light_min = (point_left - right_light_pos).normalize()
            dir_point_left_light_max = (point_left - left_light_pos).normalize()
            projection_point_left_min = point_left + dir_point_left_light_min * shadow_lenght
            projection_point_left_max = point_left + dir_point_left_light_max * light.effect_range

            # Compute right point projection
            dir_point_right_light_min = (point_right - left_light_pos).normalize()
            dir_point_right_light_max = (point_right - right_light_pos).normalize()
            projection_point_right_min = point_right + dir_point_right_light_min * shadow_lenght
            projection_point_right_max = point_right + dir_point_right_light_max * light.effect_range

            seg_left = Segment(point_left, projection_point_left_max)
            collide_res = seg_left.collide_with_segment(point_right, projection_point_right_max)
            if collide_res[0]:
                hard_projection_point_left = collide_res[1]
                hard_projection_point_right = collide_res[1]
            else:
                hard_projection_point_left = projection_point_left_max
                hard_projection_point_right = projection_point_right_max

            # Creation shadow_projection
            shadow_projection = [
                (point_left, projection_point_left_min, projection_point_left_max),
                (point_left, hard_projection_point_left),
                (point_right, hard_projection_point_right),
                (point_right, projection_point_right_min, projection_point_right_max),
            ]
        # Draw the shadow
        if self.shadowOnObject:
            pg.draw.circle(surface, (0, 0, 0, 0), position, self.radius)
        self.drawShadow(surface, shadow_projection)

        if not self.shadowOnObject:
            top_left_pos = position - vec2(self.radius, self.radius)

            circle_surface = pg.Surface((self.diameter, self.diameter), pg.SRCALPHA)
            circle_surface.fill((0, 0, 0, 0))
            pg.draw.circle(circle_surface, (255, 255, 255, 255), (self.radius, self.radius), self.radius)

            circle_surface.blit(light.surface, top_left_pos * -1, special_flags=pg.BLEND_RGBA_MULT)
            surface.blit(circle_surface, top_left_pos, special_flags=pg.BLEND_RGBA_MAX)


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
