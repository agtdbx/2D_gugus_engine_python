##############################################################################
#                                Import files                                #
##############################################################################
from terrain.lightning.shadow.Shadow import Shadow, Light, Segment


##############################################################################
#                              Import librairies                             #
##############################################################################
import pygame as pg
from pygame import Vector2 as vec2


##############################################################################
#                              Class ShadowRectangle                           #
##############################################################################
class ShadowRectangle(Shadow):
    def __init__(
            self,
            position:tuple[float, float],
            size:[int, int],
            degree:float=0,
        ) -> None:
        """
        position:tuple[float, float] -> the position of the center of the shadow obstacle
        size:[int, int] -> size of the rectangle (width, height)
        degree:float=0 -> start rotation in degrees
        """
        half_width = size[0] / 2
        half_height = size[1] / 2
        points = [
            (-half_width, -half_height),
            (half_width, -half_height),
            (half_width, half_height),
            (-half_width, half_height)
        ]
        super().__init__(
            position,
            points,
            degree,
        )


    def draw(self, surface:pg.Surface, color:tuple[int, int, int]):
        """
        Method to draw the shadow's shape for debuging
        """
        pg.draw.polygon(surface, color, self.points)


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
