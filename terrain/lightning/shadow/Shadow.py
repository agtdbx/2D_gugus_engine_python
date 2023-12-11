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


    @staticmethod
    def drawShadow(surface:pg.Surface, points:list[tuple[vec2, vec2] | None]):
        """
        surface:pg.Surface -> surface to draw shadow on it
        points:list[tuple[vec2, vec2] | None] -> list of point to draw shadown polygon

        points format :
            [proj_soft_left, proj_hard_left, proj_hard_right, proj_soft_right]
            proj_min = start of soft shadow
            proj_max = start of hard shadow
        proj format:
            (point, projection of point) or None if not exist
        """
        proj_soft_left = points[0]
        proj_hard_left = points[1]
        proj_hard_right = points[2]
        proj_soft_right = points[3]

        # Draw hard shadow
        pg.draw.polygon(surface, (0, 0, 0, 0), [proj_hard_left[0], proj_hard_left[1], proj_hard_right[1], proj_hard_right[0]])

        # Draw soft shadow
        if proj_soft_left != None and proj_soft_right != None:
            surface_soft_shadow = surface.copy()
            surface_soft_shadow.fill((255, 255, 255, 255))

            left_min_max = proj_soft_left[2] - proj_soft_left[1]
            number_of_lign_left = int(left_min_max.length()) + 1
            move_vec = left_min_max / number_of_lign_left
            alpha_minus = 255 / number_of_lign_left
            alpha = 255
            end_point = proj_soft_left[1]
            for _ in range(number_of_lign_left):
                pg.draw.line(surface_soft_shadow, (255, 255, 255, int(alpha)), proj_hard_left[0], end_point, 2)
                end_point += move_vec
                alpha = max(0, alpha - alpha_minus)

            right_min_max = proj_soft_right[2] - proj_soft_right[1]
            number_of_lign_right = int(right_min_max.length()) + 1
            move_vec = right_min_max / number_of_lign_right
            alpha_minus = 255 / number_of_lign_right
            alpha = 255
            end_point = proj_soft_right[1]
            for _ in range(number_of_lign_right):
                pg.draw.line(surface_soft_shadow, (255, 255, 255, int(alpha)), proj_hard_right[0], end_point, 2)
                end_point += move_vec
                alpha = max(0, alpha - alpha_minus)

            # In case of shadow cross
            if proj_soft_left[2] != proj_hard_left[1]:
                left_point = proj_soft_left[1].copy()
                right_point = proj_soft_right[1].copy()
                move_vec_left = proj_hard_left[1] -  proj_soft_left[2]
                move_vec_right = proj_hard_right[1] - proj_soft_right[2]

                length = int(move_vec_left.length()) + 1
                move_vec_left /= length
                move_vec_right /= length

                alpha = max(0, 255 - (alpha_minus * (number_of_lign_right - length)))
                alpha_minus = alpha / length
                for _ in range(length):
                    print(alpha)
                    pg.draw.line(surface_soft_shadow, (255, 255, 255, int(alpha)), left_point, right_point, 2)
                    left_point += move_vec_left
                    right_point += move_vec_right
                    alpha = max(0, alpha - alpha_minus)
                # pg.draw.polygon(surface_soft_shadow, (255, 255, 255, int(alpha)), [proj_hard_left[1], proj_soft_left[2], proj_soft_right[2]])

            surface.blit(surface_soft_shadow, (0, 0), None, pg.BLEND_RGBA_MULT)
            pass


##############################################################################
#                                  Functions                                 #
##############################################################################
def segment_shadow_projection(
        segment:Segment,
        light:Light,
        previous_compute_info:tuple[vec2, vec2, float] | None,
        ) -> list[tuple[vec2, vec2]] | None:
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

    # In case of hard shadow

    # Compute point position in light surface position as origin
    start = segment.start_point - light.surface_position
    end = segment.end_point - light.surface_position

    if previous_compute_info != None and previous_compute_info[0] == start:
        start_projection = previous_compute_info[1]
        distance_light_start = previous_compute_info[2]
    else:
        start_projection = None
        direction_light_start = segment.start_point - light.position
        distance_light_start = direction_light_start.length()
        direction_light_start /= distance_light_start

    end_projection = None
    direction_light_end = segment.end_point - light.position
    distance_light_end = direction_light_end.length()
    direction_light_end /= distance_light_end

    length_of_projection = light.effect_range - min(distance_light_start, distance_light_end)

    # Compute start point projection if it's not already compute, and insert it in compute list
    if start_projection == None:
        start_projection = start + direction_light_start * length_of_projection
    # Compute end point projection
    end_projection = end + direction_light_end * length_of_projection
    previous_compute_info = (end, end_projection, distance_light_end)

    shadow_points = [
        None,
        (end, end_projection),
        (start, start_projection),
        None
    ]

    return shadow_points
