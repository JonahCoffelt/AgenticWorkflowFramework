import pygame as pg


class Viewport:
    def __init__(self, ui, top: float=.1, bottom: float=.1, left: float=.1, right: float=.1):
        """
        Container for the dashboard viewport settings
        """
        
        self.ui = ui

        self.top:    float = top
        self.bottom: float = bottom
        self.left:   float = left
        self.right:  float = right

    def draw(self):
        ui = self.ui
        pg.draw.rect(ui.win, ui.preferences.secondary_color, ui.convert_rect(self.top_rect, 0))
        pg.draw.rect(ui.win, ui.preferences.secondary_color, ui.convert_rect(self.bottom_rect, 0))
        pg.draw.rect(ui.win, ui.preferences.tertiary_color, ui.convert_rect(self.left_rect), border_radius=ui.preferences.radius)
        pg.draw.rect(ui.win, ui.preferences.tertiary_color, ui.convert_rect(self.right_rect), border_radius=ui.preferences.radius)

    # Helper properties for drawing
    @property
    def rect(self) -> tuple:
        return (self.left, self.top, 1 - (self.left + self.right), 1 - (self.top + self.bottom))
    @property
    def top_rect(self) -> tuple:
        return (0, 0, 1, self.top)
    @property
    def bottom_rect(self) -> tuple:
        return (0, 1 - self.bottom, 1, self.bottom)
    @property
    def left_rect(self) -> tuple:
        return (0, self.top, self.left, 1 - (self.top + self.bottom))
    @property
    def right_rect(self) -> tuple:
        return (1 - self.right, self.top, self.right, 1 - (self.top + self.bottom))