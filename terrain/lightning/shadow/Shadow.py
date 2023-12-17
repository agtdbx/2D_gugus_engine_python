##############################################################################
#                                Import files                                #
##############################################################################
from terrain.lightning.lights.Light import Light
from engine_math.Segment import Segment
from engine_math.functions import get_normal_of_segment


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
            shadowOnObject:bool=True
        ) -> None:
        """
        position:tuple[float, float] -> the position of the center of the shadow obstacle
        shadowOnObject:bool -> If the shadow cover the object. False by default
        """
        self.position = vec2(position)
        self.shadowOnObject = shadowOnObject
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

        # Draw soft shadow both side
        if proj_soft_left != None and proj_soft_right != None:
            surface_soft_shadow = surface.copy()
            surface_soft_shadow.fill((255, 255, 255, 255))

            left_min_max = proj_soft_left[2] - proj_soft_left[1]
            right_min_max = proj_soft_right[2] - proj_soft_right[1]
            number_of_lign_left = max(int(left_min_max.length()), int(right_min_max.length())) + 1
            move_vec_left = left_min_max / number_of_lign_left
            move_vec_right = right_min_max / number_of_lign_left
            alpha_minus = 255 / number_of_lign_left
            alpha = 255
            end_point_left = proj_soft_left[1]
            end_point_right = proj_soft_right[1]
            prev_cross_polygon = None
            for _ in range(number_of_lign_left):
                if proj_soft_left[2] != proj_hard_left[1]:
                    seg_left = Segment(proj_hard_left[0], end_point_left)
                    res_left = seg_left.collide_with_segment(proj_hard_left[1], proj_soft_right[2])
                    seg_right = Segment(proj_hard_right[0], end_point_right)
                    res_right = seg_right.collide_with_segment(proj_hard_left[1], proj_soft_left[2])

                    if res_left[0] and res_right[0]:
                        color = (255, 255, 255, int(alpha))
                        pg.draw.line(surface_soft_shadow, color, proj_hard_left[0], res_left[1], 2)
                        pg.draw.line(surface_soft_shadow, color, proj_hard_right[0], res_right[1], 2)
                        if prev_cross_polygon != None:
                            pg.draw.polygon(surface_soft_shadow, (255, 255, 255, int(alpha + alpha_minus)),
                                            [res_left[1], prev_cross_polygon[0], prev_cross_polygon[1], res_right[1]])
                        prev_cross_polygon = (res_left[1], res_right[1])

                    else:
                        pg.draw.line(surface_soft_shadow, (255, 255, 255, int(alpha)), proj_hard_left[0], end_point_left, 2)
                        pg.draw.line(surface_soft_shadow, (255, 255, 255, int(alpha)), proj_hard_right[0], end_point_right, 2)

                else:
                    pg.draw.line(surface_soft_shadow, (255, 255, 255, int(alpha)), proj_hard_left[0], end_point_left, 2)
                    pg.draw.line(surface_soft_shadow, (255, 255, 255, int(alpha)), proj_hard_right[0], end_point_right, 2)
                end_point_left += move_vec_left
                end_point_right += move_vec_right
                alpha = max(0, alpha - alpha_minus)

            surface.blit(surface_soft_shadow, (0, 0), None, pg.BLEND_RGBA_MULT)

        # Draw soft shadow left side
        elif proj_soft_left != None:
            surface_soft_shadow = surface.copy()
            surface_soft_shadow.fill((255, 255, 255, 255))

            left_min_max = proj_soft_left[2] - proj_soft_left[1]
            number_of_lign_left = int(left_min_max.length()) + 1
            move_vec_left = left_min_max / number_of_lign_left
            alpha_minus = 255 / number_of_lign_left
            alpha = 255
            end_point_left = proj_soft_left[1]
            for _ in range(number_of_lign_left):
                pg.draw.line(surface_soft_shadow, (255, 255, 255, int(alpha)), proj_hard_left[0], end_point_left, 2)
                end_point_left += move_vec_left
                alpha = max(0, alpha - alpha_minus)

            surface.blit(surface_soft_shadow, (0, 0), None, pg.BLEND_RGBA_MULT)

        # Draw soft shadow right side
        elif proj_soft_right != None:
            surface_soft_shadow = surface.copy()
            surface_soft_shadow.fill((255, 255, 255, 255))

            right_min_max = proj_soft_right[2] - proj_soft_right[1]
            number_of_lign_right = int(right_min_max.length()) + 1
            move_vec_right = right_min_max / number_of_lign_right
            alpha_minus = 255 / number_of_lign_right
            alpha = 255
            end_point_right = proj_soft_right[1]
            for _ in range(number_of_lign_right):
                pg.draw.line(surface_soft_shadow, (255, 255, 255, int(alpha)), proj_hard_right[0], end_point_right, 2)
                end_point_right += move_vec_right
                alpha = max(0, alpha - alpha_minus)

            surface.blit(surface_soft_shadow, (0, 0), None, pg.BLEND_RGBA_MULT)


##############################################################################
#                                  Functions                                 #
##############################################################################
def segment_shadow_projection(
        segment:Segment,
        light:Light,
        previous_compute_info:tuple[vec2, vec2, float] | None,
        invert:bool=False
        ) -> list[tuple[vec2, vec2]] | None:
    """
    Calculate the point for create a shadow polygon
    Return None if there is no shadow
    Return the list of tupple of point. Like this :
    [
        (point, point_projected_by_shadow)
    ]
    """
    direction_light_segment = light.position - segment.center
    dist = direction_light_segment.length_squared()
    if dist == 0 or dist > light.effect_range_squared:
        return None

    dist = math.sqrt(dist)
    length_of_projection = (light.effect_range - dist) * 1.2
    direction_light_segment /= dist
    # If the light and the normal are in same direction, no shadow
    if invert:
        if direction_light_segment.dot(segment.normal) > 0:
            return None
    else:
        if direction_light_segment.dot(segment.normal) < 0:
            return None

    # Compute point position in light surface position as origin
    right = segment.start_point - light.surface_position
    left = segment.end_point - light.surface_position

    # In case of hard shadow
    if light.inner == 0:
        if previous_compute_info != None and previous_compute_info[0] == right:
            right_projection = previous_compute_info[1]
            distance_light_right = previous_compute_info[2]
        else:
            right_projection = None
            direction_light_right = segment.start_point - light.position
            distance_light_right = direction_light_right.length()
            direction_light_right /= distance_light_right

        left_projection = None
        direction_light_left = segment.end_point - light.position
        distance_light_left = direction_light_left.length()
        direction_light_left /= distance_light_left

        # Compute right point projection if it's not already compute, and insert it in compute list
        if right_projection == None:
            right_projection = right + direction_light_right * length_of_projection
        # Compute left point projection
        left_projection = left + direction_light_left * length_of_projection
        previous_compute_info = (left, left_projection, distance_light_left)

        shadow_points = [
            None,
            (left, left_projection),
            (right, right_projection),
            None
        ]

        return shadow_points

    # Soft shadow
    normal = get_normal_of_segment(segment.center, light.position)

    left_light_pos = light.position_into_surface - normal * light.inner
    right_light_pos = light.position_into_surface + normal * light.inner

    # Compute left points projections
    direction_light_left_min = (left - right_light_pos).normalize()
    direction_light_left_max = (left - left_light_pos).normalize()
    left_projection_min = left + direction_light_left_min * length_of_projection
    left_projection_max = left + direction_light_left_max * length_of_projection

    # Compute right points projections
    direction_light_right_min = (right - left_light_pos).normalize()
    direction_light_right_max = (right - right_light_pos).normalize()
    right_projection_min = right + direction_light_right_min * length_of_projection
    right_projection_max = right + direction_light_right_max * length_of_projection

    seg_left = Segment(left, left_projection_max)
    collide_res = seg_left.collide_with_segment(right, right_projection_max)
    if collide_res[0]:
        hard_projection_point_left = collide_res[1]
        hard_projection_point_right = collide_res[1]
    else:
        hard_projection_point_left = left_projection_max
        hard_projection_point_right = right_projection_max

    shadow_points = [
        (left, left_projection_min, left_projection_max),
        (left, hard_projection_point_left),
        (right, hard_projection_point_right),
        (right, right_projection_min, right_projection_max)
    ]

    return shadow_points
