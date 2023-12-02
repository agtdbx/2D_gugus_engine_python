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
#                              Class LightCircle                             #
##############################################################################
class LightCircle(Light):
	def __init__(
			self,
			position:tuple[int, int],
			inner:int,
			outer:int,
			power:int,
			color:tuple[int, int, int]=(255, 255, 255),
			radial_smooth_precision:int=100
		) -> None:
		"""
		position:tuple[int, int] -> Center of the light, in pixel (Become vec2)
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
		surface_size = vec2(self.effect_range * 2, self.effect_range * 2)
		self._create_surface(surface_size)
		self._compute_light_surface()


	def _compute_light_surface(self):
		# Compute some variable for draw smouth light
		color = [self.color.r, self.color.g, self.color.b, self.power]
		decrease_alpha = self.power / self.radial_smooth_precision
		width = self.outer / self.radial_smooth_precision
		size = width

		# Draw the full power circle if necessary
		if self.inner > 0:
			pg.draw.circle(self.surface, color, self.surface_size / 2, self.inner)
			size += self.inner

		# Draw the light smouth
		for _ in range(self.radial_smooth_precision):
			pg.draw.circle(self.surface, color, self.surface_size / 2, size, int(width * 2))
			size += width
			color[3] -= decrease_alpha
