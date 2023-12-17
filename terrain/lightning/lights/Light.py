##############################################################################
#                              Import librairies                             #
##############################################################################
import pygame as pg
from pygame import Vector2 as vec2
from abc import ABC, abstractmethod


##############################################################################
#                            Abstract class Light                            #
##############################################################################
class Light(ABC):
    def __init__(
            self,
            position:tuple[int, int],
            inner:int,
            outer:int,
            power:int,
            color:tuple[int, int, int]=(255, 255, 255),
            radial_smooth_precision:int=100,
        ) -> None:
        """
        position:tuple[int, int] -> Center of the light, in pixel (Become vec2)
        inner:int -> Radius of a circle with full power of the light
        outer:int -> Radius of the light effect, in pixel
        power:int -> Power of the light, [1, 255]
        color:tuple[int, int, int] -> Color of the light (white per default)
        radial_smooth_precision:int -> The precision of the light. More it is, more gradient you will have (100 per default)

        Abstract class to represente Lights.
        """
        self.position = vec2(position)
        self.position_into_surface = vec2(0, 0)
        self.inner = inner
        self.outer = outer
        self.power = power
        self.color = pg.Color(color)
        self.radial_smooth_precision = radial_smooth_precision

        if self.radial_smooth_precision > self.outer:
            self.radial_smooth_precision = self.outer

        self.effect_range = self.inner + self.outer
        self.effect_range_squared = self.effect_range ** 2


    def draw(self, light_surface:pg.Surface):
        """
        Methode to blit the pre-calculate draw surface on the light surface, before compute shadow.
        """
        light_surface.blit(self.surface, (0, 0))


    def _create_surface(self, surface_size):
        self.surface_size = surface_size
        self.surface = pg.Surface(self.surface_size, pg.SRCALPHA)
        self.position_into_surface = self.surface_size / 2
        self.surface_position = self.position - self.position_into_surface


    def move(self, vec:tuple):
        vec = vec2(vec)
        self.position += vec
        self.surface_position += vec


    @abstractmethod
    def _compute_light_surface(self):
        pass
