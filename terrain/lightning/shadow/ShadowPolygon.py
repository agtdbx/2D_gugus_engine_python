##############################################################################
#                                Import files                                #
##############################################################################
from terrain.lightning.shadow.Shadow import Shadow, Light, ShadowSegment
from engine_math.functions import get_normal_of_segment, clockwise_sort, get_angle


##############################################################################
#                              Import librairies                             #
##############################################################################
import pygame as pg
from pygame import Vector2 as vec2


##############################################################################
#                              Class ShadowPolygon                           #
##############################################################################
class ShadowPolygon(Shadow):
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
        # Call parent constructor
        super().__init__(position)

        # Creation lists of points
        self.circle_arround_radius = 0

        self.relative_points = []
        for point in points:
            p = vec2(point)
            dist = p.length()
            if dist > self.circle_arround_radius:
                self.circle_arround_radius = dist
            self.relative_points.append(p)

        self.number_of_points = len(self.relative_points)
        self.circle_arround_radius_squared = self.circle_arround_radius ** 2

        # Creation list of absolute points
        self.points = []
        for point in self.relative_points:
            self.points.append(point + self.position)

        self.segments = []

        if degree != 0:
            self.rotate(degree)
        else:
            self._computeSegment()


    def draw(self, surface:pg.Surface, color:tuple[int, int, int]):
        """
        Method to draw the shadow's shape for debuging
        """
        pg.draw.polygon(surface, color, self.points)


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
        for i in range(self.number_of_points):
            p1 = self.points[i - 1]
            p2 = self.points[i]
            pg.draw.line(surface, segment_color, p1, p2)
            if with_normals:
                segDir = p2 - p1
                segDir /= 2
                centrer = p1 + segDir
                normal = get_normal_of_segment(p1, p2)
                end = centrer + (normal * 5)
                pg.draw.line(surface, normal_color, centrer, end)


    def draw_shadow(
            self,
            surface:pg.Surface,
            light:Light
        ):
        """
        Method to draw the shadow on the light surface, to change light effect shape
        """
        # Check if light is not too far
        if (light.position - self.position).length_squared() - self.circle_arround_radius_squared > light.effect_range_squared:
            return
        # Compute all shadow point
        for seg in self.segments:
            shadow_projection = seg.get_shadow_projection(light)
            if shadow_projection != None:
                pg.draw.polygon(surface, (0, 0, 0, 0), shadow_projection)

        # points = []
        # points_proj = []
        # for seg in self.segments:
        #     shadow_projection = seg.get_shadow_projection(light)
        #     if shadow_projection != None:
        #         if shadow_projection[0] not in points:
        #             points.append(shadow_projection[0])
        #         if shadow_projection[3] not in points:
        #             points.append(shadow_projection[3])
        #         if shadow_projection[1] not in points_proj:
        #             points_proj.append(shadow_projection[1])
        #         if shadow_projection[2] not in points_proj:
        #             points_proj.append(shadow_projection[2])
        # points_proj.reverse()
        # points.extend(points_proj)
        # pg.draw.polygon(surface, (0, 0, 0, 0), points)
        # for p in points:
        #     pg.draw.circle(surface, (255, 255, 255), p, 2)


    def rotate(self, degrees:float):
        """
        Method to rotate the shadow by degrees
        """
        for point in self.relative_points:
            point.rotate_ip(degrees)

        self.points.clear()
        for point in self.relative_points:
            self.points.append(point + self.position)
        self._computeSegment()


    def move(self, direction:tuple[float, float] | vec2):
        """
        Method to move the shadow by pass a vector as tupple
        """
        direction = vec2(direction)
        self.position += direction
        for point in self.points:
            self.point += direction
        self._computeSegment()


    def setPosition(self, position:tuple[float, float] | vec2):
        """
        Method to set the shadow position by pass a vector as tupple
        """
        position = vec2(position)
        direction = position - self.position
        self.position = position
        for point in self.points:
            self.point += direction
        self._computeSegment()


    def _computeSegment(self):
        self.segments.clear()
        for i in range(self.number_of_points):
            p1 = self.points[i - 1]
            p2 = self.points[i]
            self.segments.append(ShadowSegment(p1, p2))
