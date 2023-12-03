##############################################################################
#                                Import files                                #
##############################################################################
from terrain.lightning.lights.Light import Light
from terrain.lightning.shadow.ShadowSegment import ShadowSegment


##############################################################################
#                              Import librairies                             #
##############################################################################
import pygame as pg
from pygame import Vector2 as vec2
from abc import ABC, abstractmethod


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
