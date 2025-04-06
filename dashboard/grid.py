import pygame as pg
import math

class Grid:
    def __init__(self, ui):
        
        # Parent references
        self.ui    = ui
        self.win   = ui.win
        
        # Surface of the grid
        self.set_surf()

        # Grid attributes
        self.scale    = 50.0
        self.position = [0.0, 0.0]

    def draw(self) -> None:
        """
        Clears and draws the grid
        """
        
        self.surf.fill(self.ui.preferences.primary_color)

        center = (self.width / 2, self.height / 2)
        self.unit     = (self.scale, self.scale)
        n_x = math.ceil(center[0] / self.unit[0])
        n_y = math.ceil(center[1] / self.unit[1])

        for x in range(-n_x, n_x + 1):
            for y in range(-n_y, n_y + 1):
                pg.draw.circle(self.surf, self.ui.preferences.tertiary_color, (center[0] + x * self.unit[0] - self.x % self.scale, center[1] + y * self.unit[1] + self.y % self.scale), (self.scale / 20) + 1)

    def show(self) -> None:
        """
        Blits the grid surfacec to the dashboard window
        """
        
        self.win.blit(self.surf, self.ui.convert_rect(self.ui.viewport.rect, 0)[:2])

    def set_surf(self) -> None:
        """
        Creates the destination surface for the grid rendering
        """
        
        self.width, self.height = self.ui.convert_rect(self.ui.viewport.rect, 0)[2:]
        self.surf = pg.Surface((self.width, self.height)).convert_alpha()

    @property
    def x(self) -> float:
        return self.position[0]
    @property
    def y(self) -> float:
        return self.position[1]
    
    @x.setter
    def x(self, value) -> None:
        self.position[0] = value
    @y.setter
    def y(self, value) -> None:
        self.position[1] = value