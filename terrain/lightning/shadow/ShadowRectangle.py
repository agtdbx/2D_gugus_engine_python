##############################################################################
#                                Import files                                #
##############################################################################
from terrain.lightning.shadow.ShadowPolygon import ShadowPolygon, Light

##############################################################################
#                              Import librairies                             #
##############################################################################
import pygame as pg
from pygame import Vector2 as vec2


##############################################################################
#                             Class ShadowRectangle                          #
##############################################################################
class ShadowRectangle(ShadowPolygon):
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
