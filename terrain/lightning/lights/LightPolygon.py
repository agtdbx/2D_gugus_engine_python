##############################################################################
#                                Import files                                #
##############################################################################
from terrain.lightning.lights.Light import Light


##############################################################################
#                              Import librairies                             #
##############################################################################
import pygame as pg
from pygame import Vector2 as vec2


##############################################################################
#                             Class LightPolygon                             #
##############################################################################
class LightPolygon(Light):
    def __init__(
            self,
            position:tuple[int, int],
            points:list[tuple[int, int]],
            inner:int,
            outer:int,
            power:int,
            color:tuple[int, int, int]=(255, 255, 255),
            radial_smooth_precision:int=100
        ) -> None:
        """
        position:tuple[int, int] -> Center of the light, in pixel (Become vec2)
        points:list[tuple[int, int]] -> List of point of form the polygon.
            The points position are relative to it's center. All point will be
            normalize. Only the shape is keep. The size is decide by inner and outer.
        inner:int -> Radius of a circle with full power of the light
        outer:int -> Radius of the light effect, in pixel
        power:int -> Power of the light, [1, 255]
        color:tuple[int, int, int] -> Color of the light (white per default)
        radial_smooth_precision:int -> The precision of the light. More it is, more gradient you will have (100 per default)
        """
        super().__init__(
            position,
            inner,
            outer,
            power,
            color,
            radial_smooth_precision
        )

        self.points = []
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        max_lenght = 0
        for p in points:
            point = vec2(p)
            if point.x < min_x:
                min_x = point.x
            if point.x > max_x:
                max_x = point.x
            if point.y < min_y:
                min_y = point.y
            if point.y > max_y:
                max_y = point.y
            lenght = point.length()
            if lenght > max_lenght:
                max_lenght = lenght
            self.points.append(point)

        for point in self.points:
            point /= max_lenght

        min_x = (min_x / max_lenght) * self.effect_range
        max_x = (max_x / max_lenght) * self.effect_range
        min_y = (min_y / max_lenght) * self.effect_range
        max_y = (max_y / max_lenght) * self.effect_range

        self.center = vec2(-min_x, -min_y)

        surface_size = vec2(max_x - min_x + 1, max_y - min_y + 1)
        self._create_surface(surface_size)

        self._compute_light_surface()


    def _compute_light_surface(self):
        # Compute some variable for draw smouth light
        color = [self.color.r, self.color.g, self.color.b, self.power]
        decrease_alpha = self.power / self.radial_smooth_precision
        width = self.outer / self.radial_smooth_precision
        size = width

        points = []

        # Draw the full power polygon if necessary
        if self.inner > 0:
            for point in self.points:
                p = point.copy()
                p *= self.inner
                p += self.center
                points.append(p)
            pg.draw.polygon(self.surface, color, points)
            size += self.inner

        # Draw the light smouth
        for _ in range(self.radial_smooth_precision):
            points.clear()
            for point in self.points:
                p = point.copy()
                p *= size
                p += self.center
                points.append(p)
            pg.draw.polygon(self.surface, color, points, int(width * 2))
            size += width
            color[3] -= decrease_alpha
